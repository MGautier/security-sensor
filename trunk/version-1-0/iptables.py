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
        
        config_file = open('./conf/iptables_conf.conf', 'r')

        self.info_config_file = {}
        for linea in config_file:
            li = linea.strip()
            regexp = re.split("\W? ", li)
            if not li.startswith("#"):
                #Lineas que NO comiencen con el símbolo '#'
                if not regexp[0] == '' :
                    #Lineas que NO contengan nada
                    key = regexp[0] #Almaceno la key del registro
                    regexp.remove('') #Elimino el espacio en blanco de la lista

                    if len(regexp) == 2:
                        self.info_config_file[""+key+""] = (regexp[1]).strip('\' ')
                    elif len(regexp) > 2:
                        regexp.remove(key)
                        #Elimino la key de la lista para concatenar como string
                        #los siguientes elementos de la misma
                        string = ""
                        for expresion in regexp:
                            string += expresion+" "

                        self.info_config_file[""+key+""] = string

        config_file.close()
        self.set_log_source()

    def processLine(self, line):
        """
        Método modificador que procesa e introduce en un bd la informacion
        relevante del filtrado de paquetes, en este caso, de iptables.
        """


        line = re.split("\W? ", line)

        register = {} #Diccionario con los valores del log iptables
        self.read_config_file()

        day_log = "" + str(date.today().year) + " " + line[0] + " " + line[1] + ""
        register["Timestamp"] = day_log + " " + str(line[2])

        if(self.check_date_bd(register["Timestamp"])):
            
            
            rows = RowsDatabase(self._db_.num_columns_table('events'))
        
            register["Timestamp_Insert_DB"] = (datetime.now()).strftime("%Y %b %d - %H:%M:%S.%f")

            self.tag_log = []
            tag_str = ((re.compile('^(.*)=')).search(str(line))).group(0)
            tag_split = tag_str.split(',')


            db_column = ['Source_IP', 'Dest_IP', 'Source_PORT', 'Dest_PORT', 'Protocol', 'Source_MAC', 'Dest_MAC']

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
                    register["Source_MAC"] =  self.regexp("Source_MAC",'MAC',str(line))
                    register["Dest_MAC"] =  self.regexp("Dest_MAC",'MAC',str(line))
                    self.tag_log.remove('MAC')
            else:
                register["Source_MAC"] = '-'
                register["Dest_MAC"] = '-'

            try:
                register["ID_IP_Source"] = self._db_.query("select ID from ips where IP = '"+"".join(register["Source_IP"])+"'")[0][0]
            except Exception as ex:
                print "ID_IP_Source Exception -> ", ex
                register["ID_IP_Source"] = '-'

            try:
                register["ID_IP_Dest"] = self._db_.query("select ID from ips where IP = '"+"".join(register["Dest_IP"])+"'")[0][0]
            except Exception as ex:
                print "ID_IP_Dest Exception -> ", ex
                register["ID_IP_Dest"] = '-'

            register["RAW_Info"] = re.sub('\[','',re.sub('\n',''," ".join(line)))
            register["TAG"] = self.get_message(line)
            register["Additional_Info"] = self.get_id_additional_info(line)

            try:
                register["ID_Log_Source"] = self._db_.query("select ID_Log_Sources from log_sources where Type = 'Iptables'")[0][0]
            except Exception as ex:
                print "ID_Log_Source Exception -> ", ex
                register["ID_Log_Source"] = '-'
           


            rows.insert_value((None,register["Timestamp"],register["Timestamp_Insert_DB"],register["Source_IP"],register["Dest_IP"],register["Source_PORT"],register["Dest_PORT"],register["Protocol"],register["Source_MAC"],register["Dest_MAC"],register["ID_IP_Source"],register["ID_IP_Dest"],register["RAW_Info"],register["Additional_Info"],register["TAG"]))

            self._db_.insert_row('events',rows)
            
            print "---> Insertado registro: " + str(register) + "\n"
            print "---> Fin de procesado de linea \n"

    def regexp(self, db_column_name, source, values):
        """
        Método que nos permite usar expresiones regulares para
        filtrar los contenidos de la línea log de iptables.
        """

        if "IP" in db_column_name:
            return self.get_ip(source,values)
        elif "PORT" in db_column_name:
            return self.get_port(source,values)
        else:
            return (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")

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

            rows.insert_value((None,_register["Description"],_register["Type"],_register["Model"],_register["Active"],_register["Software_class"],_register["Path"], _register["Info_1"], _register["Info_2"], _register["Info_3"], _register["Info_4"], _register["Info_5"], _register["Info_6"], _register["Info_7"], _register["Info_8"], _register["Info_9"], _register["Info_10"]))

            self._db_.insert_row('log_sources',rows)


    def check_date_bd(self, values):
        """
        Método para comprobar si los timestamp son consecutivos entre
        la bd y los timestamp obtenidos del log. [No se usa]
        """

        log_date = datetime.strptime(''.join(values), "%Y %b %d %H:%M:%S")
        query_bd_date = self._db_.query("select Timestamp from events where ID_events = (select max(ID_events) from events)")

        #if not query_bd_date:
        #    return True
        #else:
        #    bd_date = datetime.strptime((str(query_bd_date)).split('\'')[1], "%Y %b %d %H:%M:%S")
        #    if log_date <= bd_date:
        #        return True
        #    else:
        #        return False

        return True

    def get_id_additional_info(self, values):
        """
        Método que procesa la información necesaria para almacenarla
        en la tabla additional_info desde el log.
        """

        rows = RowsDatabase(self._db_.num_columns_table('additional_info'))
        str_values = str(values)
        string = " ".join(values)
        _register = {}


        for it in self.tag_log:
            check_value = ((re.compile(it + '=\S+')).search(str_values))
        
            if check_value:
                _register[""+it+""] = it + "="+ (((re.compile(it + '=\S+')).search(str_values)).group(0)).split(it + '=')[1].strip("',\\n\']")
            else:
                _register[""+it+""] = '-'


        if ((re.compile('URGP' + '=\S+')).search(str_values)):
            _register["URGP"] = "URGP="+((((re.compile('URGP' + '=\S+')).search(str_values)).group(0)).split('URGP' + '=')[1].strip("',\\n\']"))

        if (re.compile('ID=(.*) PROTO')).search(string):
            _register["ID"] = "ID="+(re.compile('ID=(.*) PROTO')).search(string).group(1)

        if (re.compile('RES=(.*) URGP')).search(string):
            _register["RES"] = "RES="+(re.compile('RES=(.*) URGP')).search(string).group(1)

        # Hago el diccionario anterior para controlar las distintas
        # tags que nos da el log de iptables / archivo de configuracion
        
        add_info_fields = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        add_info_fields.insert(add_info_fields.pop(0),None)
        count = 0
        string = ""
        _exit = True
        
        while _exit:
            count += 1
            field = self.info_config_file["Info_"+str(count)]
            if field in _register.keys():
                add_info_fields.insert(add_info_fields.pop(count),_register[""+field+""])
            else:
                add_info_fields.insert(add_info_fields.pop(count),'-')

            if count == 10:
                _exit = False
                
        for key in _register.keys():
            if not key in self.info_config_file.values():
                # Antes he almacenado por orden todos los Info_X, y ahora en More_Info
                # introduzco los que no coinciden con lo especificado en el archivo
                # de configuracion
                value = _register[""+key+""]
                string += ""+value+" -- "
                count += 1
        
        if count > 10:
            add_info_fields.insert(add_info_fields.pop(11),string)


        for it in add_info_fields:
            if isinstance( it, int):
                add_info_fields.insert(add_info_fields.pop(it),'-')


        rows.insert_value(tuple(add_info_fields))

        self._db_.insert_row('additional_info',rows)

        # Seleccionamos el último id de la tabla additional_info para insertar los nuevos datos
        # en orden
        
        id_query = self._db_.query("select ID_Info from additional_info where ID_Info = (select max(ID_Info) from additional_info)")

        return id_query[0][0]

    def get_message(self, values):
        """
        Método que permite almacenar el mensaje asignado a la línea de log
        de iptables.
        """

        string = " ".join(values)
        msg = self.info_config_file["Message"]
        self.tag_log.remove(msg)
        return (re.compile(''+msg+'=(.*) IN')).search(string).group(1)

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
                if hostname == '-':
                    for rdata in resolver.query(address_dns, "PTR"):
                        hostname = rdata
            except Exception as ex:
                print " "

            rows.insert_value((None, ip, hostname, '-'))
            self._db_.insert_row('ips',rows)


        return ip
