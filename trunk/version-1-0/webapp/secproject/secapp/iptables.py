#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import dns
import re
import subprocess
import socket
from django.utils import timezone
from kernel import source
# Si se borra la dependencia resolver de dns no funciona, aunque parezca que no se usa
from dns import reversename, resolver
from .models import Events, PacketEventsInformation, LogSources, Ips, Ports, Macs, PacketAdditionalInfo, Tags, Tcp
from .models import Visualizations, Udp
import calendar
from dateutil.parser import parse
from datetime import date
from configparser import ConfigParser


# Author: Moises Gautier Gomez
# Proyecto fin de carrera - Ing. en Informatica
# Universidad de Granada

class Iptables(source.Source):
    """
    Clase hija que hereda de Source para el procesamiento de información
    procedente de iptables.
    """

    def __init__(self, group=None, target=None, name=None,
                 args=(), source_info=None, verbose=None):
        """
        Metodo constructor de la clase Iptables.
        Args:
            group: por defecto su valor es None; reservado para la futura ampliacion de implementacion de la clase
            ThreadGroup
            target: es el objeto invocado por el metodo interno run(), que por defecto es None mientras nadie lo use
            name: es el nombre del hilo. Por defecto, un nombre para un hilo se construye de la forma "Thread-N",
            donde N es un numero entero decimal.
            args: es una tupla de datos usada para la invocacion del target. Por defecto es ()
            source_info: Diccionario con informacion sobre la fuente a procesar (Nombre, Archivo de configuracion,
            modelo, Archivo de log, etc)
            verbose: None

        Returns: Objeto de la clase Iptables inicializado que hereda funcionalidades de la clase Source

        """
        super(Iptables, self).__init__(group=group, target=target, name=name, args=args, source=source_info,
                                       verbose=verbose)
        # Inicializamos la clase con los parametros que se pasa como argumento al constructor y a su vez instanciamos
        # un objeto temporal para la realizacion de tareas en la clase
        # Lista que contiene las etiquetas procesadas del log de iptables
        self.tag_log = []

        # Diccionario que contiene la información extraida del archivo de configuración para iptables.
        self.info_config_file = {}

        # Objeto de la clase LogSources que sirve para almacenar informacion de la fuente en la BD
        self.log_sources = LogSources()

    def read_config_file(self):
        """
        Método modificador de la clase que abre y lee el contenido del archivo
        de configuracion para el software iptables. El contenido del archivo se
        almacena internamente en los atributos de la clase.
        Returns: None

        """

        # Instanciamos un objeto de la clase ConfigParser
        config_file = ConfigParser()

        # Abrimos el archivo de configuracion para lectura especificando la ruta relativa al archivo
        config_file.read(self.config_file)

        for it in config_file.sections():
            for it_field in config_file.items(it):
                if "tag" in it_field[0]:
                    tag_field = it_field[1].strip().split('\t')
                    # El campo de las TAG en el archivo de configuracion se divide por tabulaciones.
                    self.info_config_file[it_field[0].upper()] = [tag_field[0], tag_field[1]]
                else:
                    self.info_config_file[it_field[0].title()] = it_field[1]

        # Se establecen las tags con su descripcion para el modelo de la BD (Tag)
        self.set_tags()

        # Se establece la información perteneciente al source obtenida del archivo de configuracion
        self.set_log_source()

    @staticmethod
    def visualizations(event):
        """
        Método que nos permite ir almacenando en el modelo Visualizations el número de eventos producidos
        en una hora de un determinado día para luego extraer dicha información en la vistas de la aplicación
        Args:
            event: Objeto de la BD que contiene información de un evento asociado de Iptables

        Returns: Almacena en el modelo Visualizations la información extraida del evento.

        """

        # Creamos un objeto Visualizations con la informacion pasada como argumento al metodo

        try:
            visualizations = Visualizations.objects.get(
                Date=event['Date'],
                Hour=event['Hour'],
                ID_Source=LogSources.objects.get(Type='Iptables')
            )
            number_events = visualizations.Process_Events + 1
            Visualizations.objects.filter(pk=visualizations.pk).update(Process_Events=number_events)
            visualizations.refresh_from_db()
        # Sino hay un objeto o hay algun fallo en la creación del objeto se crea la estructura
        # completa en la bd
        except Visualizations.DoesNotExist:

            list_names_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            year = event['Date'].year
            month = event['Date'].month
            day = event['Date'].day
            week_day = calendar.weekday(year, month, day)
            week_month = 0
            count_week = 0

            for it in calendar.Calendar(0).monthdayscalendar(year, month):

                if it.count(day) == 1:
                    week_month = count_week
                else:
                    count_week += 1

            try:
                visualizations = Visualizations(
                    Week_Month=week_month,
                    Week_Day=week_day,
                    Name_Day=list_names_days[week_day],
                    Date=event['Date'],
                    Hour=event['Hour'],
                    ID_Source=LogSources.objects.get(Type='Iptables'),
                    Process_Events=1,
                )

                visualizations.save()
            except Exception as ex:
                print "visualizations -> ", ex
                print sys.exc_traceback.tb_lineno

        except Exception as ex:
            print "visualizations -> ", ex
            print sys.exc_traceback.tb_lineno

    def process_line(self, line):
        """
        Método modificador que procesa e introduce en un bd la informacion
        relevante del filtrado de paquetes, en este caso, de iptables.
        Args:
            line: Objeto file que contiene el log leido de iptables

        Returns: Muestra informacion por linea de comando de los eventos procesados y almacenados en la bd

        """

        # Se trocea por palabras el log leido
        line = re.split("\W? ", line)

        register = {}  # Diccionario con los valores del log iptables

        try:

            # timestamp tendrá cómo year el valor 1990 ya que el log no proporciona dicho valor y este lo toma
            # por defecto del tiempo unix.
            timestamp = parse(line[0])
            timestamp_insertion = timezone.now()

            tag_str = ((re.compile('^(.*)=')).search(str(line))).group(0)
            tag_split = tag_str.split(',')

            db_column = ['ID_Source_IP', 'ID_Dest_IP', 'ID_Source_PORT', 'ID_Dest_PORT', 'Protocol', 'ID_Source_MAC',
                         'ID_Dest_MAC']

            # El nombre de las tags, segun el orden de la columnas en db_column, las extraigo del fichero
            # de configuracion a traves del registro info_config_file

            labels = [self.info_config_file["Source_Ip"], self.info_config_file["Dest_Ip"],
                      self.info_config_file["Source_Port"], self.info_config_file["Dest_Port"],
                      self.info_config_file["Protocol"]]

            # Almacenamos las etiquetas o campos del log de iptables
            for it in tag_split:
                if len(it.split('=')) == 2:
                    self.tag_log.append((it.split('='))[0].strip('\' '))

            # Buscamos la correlación entre los campos definidos en la configuración con los extraidos del log
            # de iptables
            for label in labels:
                if (re.compile(label)).search(tag_str):
                    if self.tag_log.index(label) > 0:
                        db_column_name = db_column[0]
                        register[db_column.pop(0)] = self.regexp(db_column_name, label, str(line))
                        self.tag_log.remove(label)
                else:
                    register[db_column.pop(0)] = None

            if (re.compile('MAC')).search(tag_str):
                if self.tag_log.index('MAC') > 0:
                    register["ID_Source_MAC"] = self.regexp("ID_Source_MAC", 'MAC', str(line))
                    register["ID_Dest_MAC"] = self.regexp("ID_Dest_MAC", 'MAC', str(line))
                    self.tag_log.remove('MAC')
            else:
                register["ID_Source_MAC"] = None
                register["ID_Dest_MAC"] = None

            # Log en crudo
            register["RAW_Info"] = re.sub('\[', '', re.sub('\n', '', " ".join(line)))
            # Etiqueta MSG del log
            register["TAG"] = self.get_message(line)

            # Creamos una instancia del modelo Events (LogSources ya tiene una instancia
            # a traves del metodo set)

            log_sources_objects = LogSources.objects.all()

            events = Events(
                Timestamp=timestamp,
                Timestamp_Insertion=timestamp_insertion,
                ID_Source=log_sources_objects.get(Type="Iptables"),
                Comment='Iptables events',
            )
            events.save()
            date_info = date(events.Timestamp.year, events.Timestamp.month, events.Timestamp.day)
            # Dia del evento
            hour_info = events.Timestamp.hour
            # No incluyo el resto de datos porque los eventos se contabilizan por hora

            self.visualizations({'Date': date_info, 'Hour': hour_info})

            # Creamos una instancia del modelo PacketEventsInformation

            packet_events_information = PacketEventsInformation(
                ID_IP_Source=register["ID_Source_IP"],
                ID_IP_Dest=register["ID_Dest_IP"],
                ID_Source_Port=register["ID_Source_PORT"],
                ID_Dest_Port=register["ID_Dest_PORT"],
                Protocol=register["Protocol"],
                ID_Source_MAC=register["ID_Source_MAC"],
                ID_Dest_MAC=register["ID_Dest_MAC"],
                RAW_Info=register["RAW_Info"],
                TAG=register["TAG"],
                id=events,
            )
            packet_events_information.save()

            id_packet_events = packet_events_information

            self.set_packet_additional_info(line, id_packet_events)

            print "---> Insertado registro: " + str(register) + "\n"
            print "---> Fin de procesado de linea \n"
        except Exception as ex:
            print "process_line -> ", ex
            print sys.exc_traceback.tb_lineno

    def regexp(self, db_column_name, source_field, values):
        """
        Método que nos permite usar expresiones regulares para filtrar los contenidos de la línea log de iptables.
        Args:
            db_column_name: Lista con los nombres de las columnas que usa el modelo de la BD interno
            source_field: Parametro que concierne al tipo de campo (IP,MAC,PORT,MSG)
            values: Objeto string que representa una fila del log leido

        Returns: La insercion de la informacion del campo del log en la BD

        """

        if "IP" in db_column_name:
            return self.get_ip(source_field, values)
        elif "PORT" in db_column_name:
            return self.get_port(source_field, values)
        elif "MAC" in db_column_name:
            return self.get_mac(source_field, values)
        else:
            return (((re.compile(source_field + '=\S+')).search(values)).group(0)).split(source_field + '=')[1].strip("',")

    @staticmethod
    def get_ip(source_field, values):
        """
        Método que permite extraer información de la ip del log desde el propio sistema
        o obteniendola de la red.
        Args:
            source_field: Parametro que concierne al tipo de campo (IP,MAC,PORT,MSG)
            values: Objeto string que representa una fila del log leido

        Returns: La insercion de la informacion de IP en la BD y como resultado el identificador de la fila insertada

        """

        ips_objects = Ips.objects.all()
        ip = (((re.compile(source_field + '=\S+')).search(values)).group(0)).split(source_field + '=')[1].strip("',")
        id_ip = 0

        for it in ips_objects:
            if it.Ip == ip:
                id_ip = it

        # Aquí lo que hago es comprobar si existe una ip similar en la
        # tabla. Si no existe se inserta un nuevo registro de ip en la tabla.
        if not id_ip:

            hostname = '-'

            try:
                hostname, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
            except socket.error as msg:
                print "Get_ip -> ", msg

            try:
                address_dns = reversename.from_address(str(ip))
                # Incluyo las siguientes lineas para dotar de menor tiempo
                # de procesamiento de resolucion de dns
                resolver = dns.resolver.Resolver()
                resolver.timeout = 1
                resolver.lifetime = 1
                if hostname == '-':
                    for rdata in resolver.query(address_dns, "PTR"):
                        hostname = rdata

                ips = Ips(
                    Ip=ip,
                    Hostname=hostname,
                    Tag='-',
                )

                ips.save()
                id_ip = ips
            except Exception as ex:
                print "get_ip -> ", ex

        return id_ip

    @staticmethod
    def get_port(source_field, values):
        """
        Método que permite extraer información de los puertos con los que iptables
        está trabajando desde el sistema (si es que hay información asociada a ellos)
        Args:
            source_field: Parametro que concierne al tipo de campo (IP,MAC,PORT,MSG)
            values: Objeto string que representa una fila del log leido

        Returns: La insercion de la informacion de PORT en la BD y como resultado el identificador del
        puerto insertado

        """

        ports = Ports.objects.all()
        # Realizamos una comprobacion previa sobre el modelo por si existiera un puerto similar anteriormente
        # insertado, sino se crea con todos los campos relacionados.
        port_regex = (((re.compile(source_field + '=\S+')).search(values)).group(0)).split(source_field + '=')[1].strip("',")
        id_ports = 0
        for it in ports:
            if it.id == port_regex:
                id_ports = it

        # Extraemos el tipo de servicio que presta el puerto en nuestra maquina (para sistemas unix)
        p = subprocess.Popen(["grep -w " + port_regex + " /etc/services"], stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        grep_port = (output.split('\n'))

        if id_ports == 0:

            if len(grep_port[0]) == 0:
                new_port = Ports(
                    id=port_regex,
                    Tag='-',
                )
                new_port.save()
                id_ports = new_port

            # Si el puerto es para tráfico TCP
            if len(grep_port[0]) != 0:
                port_1 = grep_port[0].split('\t')
                port_number = (grep_port[0].split('\t'))[2].split('/')[0]
                port_protocol = (grep_port[0].split('\t'))[2].split('/')[1]
                if len((grep_port[0].split('# '))) > 1:
                    port_description = (grep_port[0].split('# '))[1]
                else:
                    port_description = '-'

                if len(port_1) > 3:
                    if port_1[4] != '':
                        port_service = port_1[4]
                    else:
                        port_service = '-'
                else:
                    port_service = '-'

                if port_number == port_regex:
                    new_port = Ports(
                        id=port_regex,
                        Tag=port_1[0],
                    )
                    new_port.save()
                    id_ports = new_port
                    new_tcp = Tcp(
                        id=new_port,
                        Service=port_service,
                        Description=port_description,
                    )
                    new_tcp.save()

                # Si el puerto es para tráfico UDP
                if len(grep_port) > 1:
                    if len(grep_port[1]) != 0:
                        port_2 = grep_port[1].split('\t')

                        port_number = (grep_port[1].split('\t'))[2].split('/')[0]
                        port_protocol = (grep_port[1].split('\t'))[2].split('/')[1]

                        if len((grep_port[1].split('# '))) > 1:
                            port_description = (grep_port[1].split('# '))[1]
                        else:
                            port_description = '-'

                        if len(port_2) > 3:
                            if port_2[4] != '':
                                port_service = port_2[4]
                            else:
                                port_service = '-'
                        else:
                            port_service = '-'

                        if port_number == port_regex:
                            new_udp = Udp(
                                id=new_port,
                                Service=port_service,
                                Description=port_description,
                            )

                            new_udp.save()
        return id_ports

    @staticmethod
    def get_mac(source_field, values):
        """
        Método que establece el contenido de la tabla macs a través de la información proporcionada por iptables.
        Args:
            source_field: Parametro que concierne al tipo de campo (IP,MAC,PORT,MSG)
            values: Objeto string que representa una fila del log leido

        Returns: La insercion de la informacion de MAC en la BD y como resultado el identificador de la MAC insertada

        """

        macs = Macs.objects.all()
        mac = (((re.compile(source_field + '=\S+')).search(values)).group(0)).split(source_field + '=')[1].strip("',")

        id_macs = 0
        for it in macs:
            if it.MAC == mac:
                id_macs = it

        if not id_macs:
            new_mac = Macs(
                MAC=mac,
                TAG='-',
            )
            new_mac.save()
            id_macs = new_mac

        return id_macs

    def set_tags(self):
        """
        Método que establece el contenido de la tabla tags una vez ha comenzado el procesamiento del log de
        iptables. Dicho contenido lo extraemos del archivo de configuración.
        Returns: None

        """

        for it in self.info_config_file:
            if "TAG_" in it:
                tags = Tags(
                    id=it.strip("TAG_"),
                    Description=self.info_config_file[it][1],
                    Tag=self.info_config_file[it][0]
                )
                tags.save()

    def set_log_source(self):
        """
        Método que establece el contenido de la tabla log_sources una
        vez ha comenzado el procesamiento del log de iptables.
        Returns: None

        """

        log_sources_objects = LogSources.objects.all()
        validation = True

        # Caso 1: No existe objeto alguno en la bd
        if not log_sources_objects:
            self.log_sources = LogSources(
                Description=self.info_config_file["Description"],
                Type=self.info_config_file["Type"],
                Model=self.info_config_file["Model"],
                Active=self.info_config_file["Active"],
                Software_Class=self.info_config_file["Software_Class"],
                Path=self.info_config_file["Path"],
            )
            self.log_sources.save()
        else:
            # Caso 2: Comprobar que objetos hay ya en log_source para
            # evitar duplicaciones compruebo la ruta o comando
            # para la activacion del software

            for it in log_sources_objects:
                if it.Path == self.info_config_file["Path"]:
                    validation = False

            if validation:
                self.log_sources = LogSources(
                    Description=self.info_config_file["Description"],
                    Type=self.info_config_file["Type"],
                    Model=self.info_config_file["Model"],
                    Active=self.info_config_file["Active"],
                    Software_class=self.info_config_file["Software_Class"],
                    Path=self.info_config_file["Path"],
                )
                self.log_sources.save()

    def set_packet_additional_info(self, values, id_packet_event):
        """
        Método que procesa la información necesaria para almacenarla en la tabla packet_additional_info desde el log.
        Args:
            values: Objeto string que representa una fila del log leido
            id_packet_event: Identificador del objeto PacketEvents que se relaciona con su informacion de paquete
        adicional

        Returns:

        """

        tags_objects = Tags.objects.all()

        str_values = str(values)
        string = " ".join(values)
        _register = {}

        for it in self.tag_log:
            check_value = ((re.compile(it + '=\S+')).search(str_values))

            if check_value:
                _register["" + it + ""] = (((re.compile(it + '=\S+')).search(str_values)).group(0)).split(it + '=')[
                    1].strip("',\\n\']")
            else:
                _register["" + it + ""] = '-'

        if (re.compile('URGP' + '=\S+')).search(str_values):
            _register["URGP"] = (
                (((re.compile('URGP' + '=\S+')).search(str_values)).group(0)).split('URGP' + '=')[1].strip("',\\n\']"))

        if (re.compile('ID=(.*) PROTO')).search(string):
            _register["ID"] = (re.compile('ID=(.*) PROTO')).search(string).group(1)

        if (re.compile('RES=(.*) URGP')).search(string):
            _register["RES"] = (re.compile('RES=(.*) URGP')).search(string).group(1)

        # Hago el diccionario anterior para controlar las distintas
        # tags que nos da el log de iptables / archivo de configuracion

        for it in _register:
            for it_tag in tags_objects:
                if it_tag.Tag == it:
                    packet_additional = PacketAdditionalInfo(
                        ID_Tag=it_tag,
                        ID_Packet_Events=id_packet_event,
                        Value=_register[it],
                    )
                    packet_additional.save()

    def get_message(self, values):
        """
        Método que permite almacenar el mensaje asignado a la línea de log
        de iptables.
        Args:
            values: Objeto string que representa una fila del log leido

        Returns: Se devuelve un objeto string con la cadena de texto del campo MSG del log procesado

        """

        string = " ".join(values)
        msg = self.info_config_file["Message"]
        self.tag_log.remove(msg)
        return (re.compile('' + msg + '=(.*) IN')).search(string).group(1)
