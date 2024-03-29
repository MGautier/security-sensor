#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import re
import subprocess
import socket
import time
from source import Source
from datetime import date
from datetime import datetime
from rowsdatabase import RowsDatabase
from dns import resolver, reversename

# Author: Moisés Gautier Gómez
# Proyecto fin de carrera - Ing. en Informática
# Universidad de Granada



class Iptables(Source):

    """
    Clase hija que hereda de Source para el procesamiento de información
    procedente de iptables.
    """

    def read_config_file(self):
        """
        Método modificador de la clase que abre y lee el contenido del archivo
        de configuracion para el software iptables. El contenido del archivo se
        almacena internamente en los atributos de la clase.
        """

        file = open(self.config_file, 'r')
        self.info_config_file = {}

        for linea in file.readlines():

            pline = linea.strip().split('\t')

            if pline[0] != '' and pline[0][0] != '#':
                if "TAG_" in pline[0]:
                    self.info_config_file[pline[0]] = [pline[1],pline[2]]
                else:
                    self.info_config_file[pline[0]] = pline[1]

        file.close()
        self.set_tags()
        self.set_log_source()

    def processLine(self, line):
        """
        Método modificador que procesa e introduce en un bd la informacion
        relevante del filtrado de paquetes, en este caso, de iptables.
        """

        line = re.split("\W? ", line)

        register = {} #Diccionario con los valores del log iptables

        try:

            Timestamp = line[0] + ' ' + line[1] + ' ' + line[2]
            Timestamp_Insertion = (datetime.now()).strftime("%Y %b %d - %H:%M:%S.%f")

            rows = RowsDatabase(self._db_.num_columns_table('packet_events_information'))



            self.tag_log = []
            tag_str = ((re.compile('^(.*)=')).search(str(line))).group(0)
            tag_split = tag_str.split(',')


            db_column = ['ID_Source_IP', 'ID_Dest_IP', 'ID_Source_PORT', 'ID_Dest_PORT', 'Protocol', 'ID_Source_MAC', 'ID_Dest_MAC']

            # El nombre de las tags, segun el orden de la columnas en db_column, las extraigo del fichero
            # de configuracion a traves del registro info_config_file
            
            etiquetas = [self.info_config_file["Source_IP"],  self.info_config_file["Dest_IP"], self.info_config_file["Source_PORT"], self.info_config_file["Dest_PORT"], self.info_config_file["Protocol"]]

            for iter in tag_split:
                if len(iter.split('=')) == 2:
                    self.tag_log.append((iter.split('='))[0].strip('\' '))


            for etiqueta in etiquetas:
                if (re.compile(etiqueta)).search(tag_str):
                    if self.tag_log.index(etiqueta) > 0:
                        db_column_name = db_column[0]
                        register[db_column.pop(0)] = self.regexp(db_column_name,etiqueta,str(line))
                        self.tag_log.remove(etiqueta)
                else:
                    register[db_column.pop(0)] = '-'
					


            if (re.compile('MAC')).search(tag_str):
                if self.tag_log.index('MAC') > 0:
                    register["ID_Source_MAC"] =  self.regexp("ID_Source_MAC",'MAC',str(line))
                    register["ID_Dest_MAC"] =  self.regexp("ID_Dest_MAC",'MAC',str(line))
                    self.tag_log.remove('MAC')
            else:
                register["ID_Source_MAC"] = '-'
                register["ID_Dest_MAC"] = '-'

            register["RAW_Info"] = re.sub('\[','',re.sub('\n',''," ".join(line)))
            register["TAG"] = self.get_message(line)



            rows.insert_value((None,register["ID_Source_IP"],register["ID_Dest_IP"],register["ID_Source_PORT"],register["ID_Dest_PORT"],register["Protocol"],register["ID_Source_MAC"],register["ID_Dest_MAC"],register["RAW_Info"],register["TAG"]))

            self._db_.insert_row('packet_events_information',rows)

            id_packet_events = self._db_.query("select ID from packet_events_information where ID =(select max(ID) from packet_events_information)")

            self.set_packet_additional_info(line, id_packet_events)
            row_events = RowsDatabase(self._db_.num_columns_table('events'))

            try:
                ID_Source = self._db_.query("select ID_Log_Sources from log_sources where Type = 'Iptables'")[0][0]
            except Exception as ex:
                print "ID_Source Exception -> ", ex
                ID_Source = '-'

            Comment = 'Iptables'
            row_events.insert_value((None, Timestamp, Timestamp_Insertion, ID_Source, Comment))
            self._db_.insert_row('events',row_events)
            
            print "---> Insertado registro: " + str(register) + "\n"
            print "---> Fin de procesado de linea \n"
        except Exception as ex:
            print "ProcessLine -> ", ex

    def regexp(self, db_column_name, source, values):
        """
        Método que nos permite usar expresiones regulares para
        filtrar los contenidos de la línea log de iptables.
        """

        if "IP" in db_column_name:
            return self.get_ip(source,values)
        elif "PORT" in db_column_name:
            return self.get_port(source,values)
        elif "MAC" in db_column_name:
            return self.get_mac(source,values)
        else:
            return (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")

    def get_ip(self, source, values):
        """
        Método que permite extraer información de la ip del log desde el propio sistema
        o obteniendola de la red."""

        ip = (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")
        id_ip = self._db_.query("select ID from ips where IP = '"+ip+"'")

        #Aquí lo que hago es comprobar si existe una ip similar en la
        # tabla. Si no existe se inserta un nuevo registro de ip en la tabla.
        if not id_ip:
            
            hostname = '-'
            rows = RowsDatabase(self._db_.num_columns_table('ips'))
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
            except Exception as ex:
                print " "

            rows.insert_value((None, ip, hostname, '-'))
            self._db_.insert_row('ips',rows)
            id_ip = self._db_.query("select ID from ips where IP = '"+ip+"'")


        return id_ip[0][0]

    def get_port(self, source, values):
        """
        Método que permite extraer información de los puertos con los que iptables
        está trabajando desde el sistema (si es que hay información asociada a ellos)
        """

        port_bd = (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")

        rows = RowsDatabase(self._db_.num_columns_table('ports'))

        id_ports = self._db_.query("select count(*) from ports where ID_PORT = '"+port_bd+"'")

        p = subprocess.Popen(["grep -w "+port_bd+" /etc/services"], stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        grep_port = (output.split('\n'))


        if (id_ports[0][0] == 0):
            

            if len(grep_port[0]) == 0 :
                rows.insert_value((port_bd, '-', '-', '-', '-'))
            
            #TCP
            if len(grep_port[0]) != 0 :
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

                if port_number == port_bd :

                    rows.insert_value((port_bd, port_protocol, port_service, port_description, port_1[0]))

            #UDP
            if len(grep_port) > 1:
                if len(grep_port[1]) != 0 :
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
                        
                    if port_number == port_bd :

                        rows.insert_value((port_bd, port_protocol, port_service, port_description, port_2[0]))


            if rows.get_length() > 0:
                self._db_.insert_row('ports',rows)

        return eval(str(port_bd))

    def get_mac(self, source, values):
        """
        Método que establece el contenido de la tabla macs
        a través de la información proporcionada por iptables.
        """

        mac = (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")

        rows = RowsDatabase(self._db_.num_columns_table('macs'))

        id_macs = self._db_.query("select ID from macs where MAC = '"+mac+"'")

        if not id_macs:
            rows.insert_value((None,mac,'-'))
            self._db_.insert_row('macs',rows)
            id_macs = self._db_.query("select ID from macs where MAC = '"+mac+"'")

        return id_macs[0][0]

    def set_tags(self):
        """
        Método que establece el contenido de la tabla tags una vez
        ha comenzado el procesamiento del log de iptables. Dicho contenido
        lo extraemos del archivo de configuración.
        """

        rows = RowsDatabase(self._db_.num_columns_table('tags'))

        for it in self.info_config_file:
            if "TAG_" in it:
               rows.insert_value((it.strip("TAG_"),self.info_config_file[it][0],self.info_config_file[it][1]))

        self._db_.insert_row('tags', rows)
        
    def set_log_source(self):
        """
        Método que establece el contenido de la tabla log_sources una
        vez ha comenzado el procesamiento del log de iptables.
        """

        rows = RowsDatabase(self._db_.num_columns_table('log_sources'))
        _register = {}
        _query_bd = self._db_.query("select ID_Log_Sources from log_sources where Type ='Iptables'")
        if not _query_bd:

            for it in self._db_.columns_name_tables('log_sources'):
                if not ("ID" in it) | ("More_Info" in it):
                    _register[""+it+""] = self.info_config_file[""+it+""]

            rows.insert_value((None,_register["Description"],_register["Type"],_register["Model"],_register["Active"],_register["Software_class"],_register["Path"]))

            self._db_.insert_row('log_sources',rows)


    def set_packet_additional_info(self, values, id_packet_event):
        """
        Método que procesa la información necesaria para almacenarla
        en la tabla packet_additional_info desde el log.
        """

        rows = RowsDatabase(self._db_.num_columns_table('packet_additional_info'))
        str_values = str(values)
        string = " ".join(values)
        _register = {}


        for it in self.tag_log:
            check_value = ((re.compile(it + '=\S+')).search(str_values))
        
            if check_value:
                _register[""+it+""] = (((re.compile(it + '=\S+')).search(str_values)).group(0)).split(it + '=')[1].strip("',\\n\']")
            else:
                _register[""+it+""] = '-'


        if ((re.compile('URGP' + '=\S+')).search(str_values)):
            _register["URGP"] = ((((re.compile('URGP' + '=\S+')).search(str_values)).group(0)).split('URGP' + '=')[1].strip("',\\n\']"))

        if (re.compile('ID=(.*) PROTO')).search(string):
            _register["ID"] = (re.compile('ID=(.*) PROTO')).search(string).group(1)

        if (re.compile('RES=(.*) URGP')).search(string):
            _register["RES"] = (re.compile('RES=(.*) URGP')).search(string).group(1)

        # Hago el diccionario anterior para controlar las distintas
        # tags que nos da el log de iptables / archivo de configuracion
        
        
        for it in _register:
            
            rows.insert_value((id_packet_event[0][0], it, _register[it]))


        self._db_.insert_row('packet_additional_info',rows)


    def get_message(self, values):
        """
        Método que permite almacenar el mensaje asignado a la línea de log
        de iptables.
        """

        string = " ".join(values)
        msg = self.info_config_file["Message"]
        self.tag_log.remove(msg)
        return (re.compile(''+msg+'=(.*) IN')).search(string).group(1)

