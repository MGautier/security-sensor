#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import dns
import re
import subprocess
import socket
import time
from django.utils import timezone
from datetime import datetime
from kernel import rowsdatabase, source
from dns import resolver, reversename
from .models import Events, PacketEventsInformation, LogSources, Ips, Ports, Macs, PacketAdditionalInfo, Tags, Tcp, Udp
from dateutil.parser import parse


# Author: Moisés Gautier Gómez
# Proyecto fin de carrera - Ing. en Informática
# Universidad de Granada

class Iptables(source.Source):
    """
    Clase hija que hereda de Source para el procesamiento de información
    procedente de iptables.
    """

    def __init__(self, group=None, target=None, name=None,
                 args=(), source=None, verbose=None):
        super(Iptables, self).__init__(group=group, target=target, name=name, args=args, source=source, verbose=verbose)
        self.tag_log = []
        self.info_config_file = {}
        self.log_sources = LogSources()

    def read_config_file(self):
        """
        Método modificador de la clase que abre y lee el contenido del archivo
        de configuracion para el software iptables. El contenido del archivo se
        almacena internamente en los atributos de la clase.
        """

        config_file = open(self.config_file, 'r')

        for linea in config_file.readlines():

            line_process = linea.strip().split('\t')

            if line_process[0] != '' and line_process[0][0] != '#':
                if "TAG_" in line_process[0]:
                    self.info_config_file[line_process[0]] = [line_process[1], line_process[2]]
                else:
                    self.info_config_file[line_process[0]] = line_process[1]

        config_file.close()
        self.set_tags()
        self.set_log_source()

    def process_line(self, line):
        """
        Método modificador que procesa e introduce en un bd la informacion
        relevante del filtrado de paquetes, en este caso, de iptables.
        :type line: object string
        :param line:
        """

        line = re.split("\W? ", line)

        register = {}  # Diccionario con los valores del log iptables

        try:

            # timestamp tendrá cómo year el valor 1990 ya que el log no proporciona dicho valor y este lo toma
            # por defecto del tiempo unix.
            timestamp = parse(line[0])
            timestamp_insertion = timezone.now()
            events = Events(
                Timestamp=timestamp,
                Timestamp_Insertion=timestamp_insertion,

            )

            tag_str = ((re.compile('^(.*)=')).search(str(line))).group(0)
            tag_split = tag_str.split(',')

            db_column = ['ID_Source_IP', 'ID_Dest_IP', 'ID_Source_PORT', 'ID_Dest_PORT', 'Protocol', 'ID_Source_MAC',
                         'ID_Dest_MAC']

            # El nombre de las tags, segun el orden de la columnas en db_column, las extraigo del fichero
            # de configuracion a traves del registro info_config_file

            labels = [self.info_config_file["Source_IP"], self.info_config_file["Dest_IP"],
                      self.info_config_file["Source_PORT"], self.info_config_file["Dest_PORT"],
                      self.info_config_file["Protocol"]]

            for it in tag_split:
                if len(it.split('=')) == 2:
                    self.tag_log.append((it.split('='))[0].strip('\' '))

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

            register["RAW_Info"] = re.sub('\[', '', re.sub('\n', '', " ".join(line)))
            register["TAG"] = self.get_message(line)

            # Creamos una instancia del modelo Events (LogSources ya tiene una instancia
            # a traves del metodo set

            log_sources_objects = LogSources.objects.all()

            events = Events(
                Timestamp=timestamp,
                Timestamp_Insertion=timestamp_insertion,
                ID_Source=log_sources_objects.get(Type="Iptables"),
                Comment='Iptables events',
            )
            events.save()

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

    def regexp(self, db_column_name, source, values):
        """
        Método que nos permite usar expresiones regulares para
        filtrar los contenidos de la línea log de iptables.
        :param source:
        :param values:
        :return:
        :param db_column_name:
        """

        if "IP" in db_column_name:
            return self.get_ip(source, values)
        elif "PORT" in db_column_name:
            return self.get_port(source, values)
        elif "MAC" in db_column_name:
            return self.get_mac(source, values)
        else:
            return (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")

    @staticmethod
    def get_ip(source, values):
        """
        Método que permite extraer información de la ip del log desde el propio sistema
        o obteniendola de la red.
        :param source:
        :param values:
        :return: """

        ips_objects = Ips.objects.all()
        ip = (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")
        id_ip = 0

        for it in ips_objects:
            if it.Ip == ip:
                id_ip = it

        # Aquí lo que hago es comprobar si existe una ip similar en la
        # tabla. Si no existe se inserta un nuevo registro de ip en la tabla.
        if not id_ip:

            hostname = '-'
            aliaslist = '-'
            ipaddrlist = ""
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
    def get_port(source, values):
        """
        Método que permite extraer información de los puertos con los que iptables
        está trabajando desde el sistema (si es que hay información asociada a ellos)
        :param source:
        :param values:
        :return:
        """

        ports = Ports.objects.all()

        port_regex = (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")
        id_ports = 0
        for it in ports:
            if it.id == port_regex:
                id_ports = it

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

            # TCP
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

                # UDP
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
    def get_mac(source, values):
        """
        Método que establece el contenido de la tabla macs
        a través de la información proporcionada por iptables.
        :param source:
        :param values:
        :return:
        """

        macs = Macs.objects.all()
        mac = (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")

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
        Método que establece el contenido de la tabla tags una vez
        ha comenzado el procesamiento del log de iptables. Dicho contenido
        lo extraemos del archivo de configuración.
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
                Software_Class=self.info_config_file["Software_class"],
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
                    Software_class=self.info_config_file["Software_class"],
                    Path=self.info_config_file["Path"],
                )
                self.log_sources.save()

    def set_packet_additional_info(self, values, id_packet_event):
        """
        Método que procesa la información necesaria para almacenarla
        en la tabla packet_additional_info desde el log.
        :param values:
        :param id_packet_event:
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
        :param values:
        :return:
        """

        string = " ".join(values)
        msg = self.info_config_file["Message"]
        self.tag_log.remove(msg)
        return (re.compile('' + msg + '=(.*) IN')).search(string).group(1)
