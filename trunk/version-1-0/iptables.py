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


class Iptables(Source):

    def processLine(self, line):


        line = re.split("\W? ", line)
        register = {} #Diccionario con los valores del log iptables

        self.day_log = "" + str(date.today().year) + " " + line[0] + " " + line[1] + ""
        register["Timestamp"] = self.day_log + " " + str(line[2])
        if(self.check_date_bd(register["Timestamp"])):
            
            
            rows = RowsDatabase(self._db_.num_columns_table('events'))
        
            register["Timestamp_Insert_DB"] = (datetime.now()).strftime("%Y %b %d - %H:%M:%S.%f")

            #ahora = datetime.strptime(''.join(self.register["Timestamp"]), "%Y %b %d %H:%M:%S")
            #despues = datetime.now()
            #print "Ahora: ", ahora
            #print "Despues: ", despues
            #print ahora > despues

            self.tag_log = []
            tag_str = ((re.compile('^(.*)=')).search(str(line))).group(0)
            tag_split = tag_str.split(',')

            etiquetas = ['SRC',  'DST', 'SPT', 'DPT', 'PROTO']
            db_column = ['Source_IP', 'Dest_IP', 'Source_PORT', 'Dest_PORT', 'Protocol']

            for iter in tag_split:
                if len(iter.split('=')) == 2:
                    self.tag_log.append((iter.split('='))[0].strip('\' '))


            for etiqueta in etiquetas:
                if (re.compile(etiqueta)).search(tag_str):
                    if self.tag_log.index(etiqueta) > 0:
                        register[db_column.pop(0)] = self.get_ip(etiqueta,str(line))
                        self.tag_log.remove(etiqueta)
                else:
                    register[db_column.pop(0)] = '-'
					


            if (re.compile('MAC')).search(tag_str):
                if self.tag_log.index('MAC') > 0:
                    register["Source_MAC"] =  self.regexp('MAC',str(line))
                    register["Dest_MAC"] =  self.regexp('MAC',str(line))
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
            register["TAG"] = self.get_tag(line)
            #Introducir los datos en una fila de la tabla Process y pasar el id a dicha entrada
            register["Additional_Info"] = self.get_id_additional_info(line)
            register["ID_Source_Log"] = '-'


            rows.insert_value((None,register["Timestamp"],register["Timestamp_Insert_DB"],register["Source_IP"],register["Dest_IP"],register["Source_PORT"],register["Dest_PORT"],register["Protocol"],register["Source_MAC"],register["Dest_MAC"],register["ID_IP_Source"],register["ID_IP_Dest"],register["RAW_Info"],register["Additional_Info"],register["TAG"]))

            self._db_.insert_row('events',rows)
            
            print "---> Insertado registro: " + str(register)
            print "---> Fin de procesado de linea"

    def regexp(self, source, values):

        return (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")

    def check_date_bd(self, values):

		log_date = datetime.strptime(''.join(values), "%Y %b %d %H:%M:%S")
        #bd_date = datetime.strptime(''.join(self._db_.query("select Timestamp from events where ID_events = (select max(ID_events) from events)")), "%Y %b %d %H:%M:%S")

		print "FECHA ", self._db_.query("select Timestamp from events where ID_events = (select max(ID_events) from events)")
		print "LOG-DATE: ", log_date
		#print "BD-DATE: ", bd_date
		#print log_date > bd_date
		return True
		#return log_date > bd_date

    def get_id_additional_info(self, values):

        rows = RowsDatabase(self._db_.num_columns_table('additional_info'))
        str_values = str(values)
        string = " ".join(values)
        info_dict = {}
        
        for it in self.tag_log:
            check_value = ((re.compile(it + '=\S+')).search(str_values))

            if check_value:
                info_dict[""+it+""] = it + "="+ (((re.compile(it + '=\S+')).search(str_values)).group(0)).split(it + '=')[1].strip("',\\n\']")
            else:
                info_dict[""+it+""] = '-'


        if ((re.compile('URGP' + '=\S+')).search(str_values)):
            info_dict["URGP"] = "URGP="+((((re.compile('URGP' + '=\S+')).search(str_values)).group(0)).split('URGP' + '=')[1].strip("',\\n\']"))

        if (re.compile('ID=(.*) PROTO')).search(string):
            info_dict["ID"] = "ID="+(re.compile('ID=(.*) PROTO')).search(string).group(1)

        if (re.compile('RES=(.*) URGP')).search(string):
            info_dict["RES"] = "RES="+(re.compile('RES=(.*) URGP')).search(string).group(1)

        # Hago el diccionario anterior para controlar las distintas
        # tags que nos da el log de iptables
        
        info_process = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        info_process.insert(info_process.pop(0),None)
        count = 0
        more_info_string = ""
        for it in info_dict.values():
            if count <= 9:
                count += 1
                info_process.insert(info_process.pop(count),it)
            else:
                more_info_string += ""+it+" -- "
                count += 1

        if count > 10:
            info_process.insert(info_process.pop(11),more_info_string)


        for it in info_process:
            if isinstance( it, int):
                info_process.insert(info_process.pop(it),'-')

        rows.insert_value(tuple(info_process))

        self._db_.insert_row('additional_info',rows)

        # Si se vuelve a ejecutar cogerá los ids nuevos y no los ya
        # almacenados en la bd.
        
        id_query = self._db_.query("select ID_Info from process where ID_Info = (select max(ID_Info) from process)")

        return id_query[0][0]

    def get_tag(self, values):

        self.string = " ".join(values)
        self.tag_log.remove('IPTMSG')
        return (re.compile('IPTMSG=(.*) IN')).search(self.string).group(1)

    def get_port(self, source, values):

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

                    print "PORT 1 ", port_1
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

                        print "PORT 2 ", port_2
                        rows.insert_value((port_bd, port_protocol, port_service, port_description, port_2[0]))


            if rows.get_length() > 0:
                self._db_.insert_row('ports',rows)

        return eval(str(port_bd))

    def get_ip(self, source, values):

        hostname = (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")
        #print "HOST: ", hostname
        rows = RowsDatabase(self._db_.num_columns_table('ips'))
        aliaslist = "TAG"
        #self.ipaddrlist = ""
        #try:
        #    self.hostname, self.aliaslist, self.ipaddrlist = socket.gethostbyaddr(self.ip_result)
        #except socket.error as msg:
        #    print msg
        
        #self.rows.insert_value((self.ip_result, self.hostname, ))
        
        id_ip = self._db_.query("select ID from ips where IP = '"+hostname+"'")

        #Aquí lo que hago es comprobar si existe una ip similar en la
        # tabla. Si la hay introduzco en el mismo id el valor, y sino
        # se inserta un nuevo registro de ip en la tabla.
        
        if id_ip:
            rows.insert_value((id_ip[0][0], hostname, aliaslist))
        else:
            rows.insert_value((None, hostname, aliaslist))
        
        self._db_.insert_row('ips',rows)


        return hostname
