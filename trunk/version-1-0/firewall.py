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


class Firewall(Source):

    def processLine(self, line):


        line = re.split("\W? ", line)
        register = {} #Diccionario con los valores del log iptables

        self.day_log = "" + str(date.today().year) + " " + line[0] + " " + line[1] + ""
        register["Timestamp"] = self.day_log + " " + str(line[2])
        if(self.check_date_bd(register["Timestamp"])):
            
            
            rows = RowsDatabase(self._db_.num_columns_table('events'))
        
            register["Timestamp_insert"] = (datetime.now()).strftime("%Y %b %d - %H:%M:%S.%f")

            #ahora = datetime.strptime(''.join(self.register["Timestamp"]), "%Y %b %d %H:%M:%S")
            #despues = datetime.now()
            #print "Ahora: ", ahora
            #print "Despues: ", despues
            #print ahora > despues

            self.tag_log = []
            tag_str = ((re.compile('^(.*)=')).search(str(line))).group(0)
            tag_split = tag_str.split(',')

            for iter in tag_split:
                if len(iter.split('=')) == 2:
                    self.tag_log.append((iter.split('='))[0].strip('\' '))

            if (re.compile('SRC')).search(tag_str):
                if self.tag_log.index('SRC') > 0:
                    register["S_IP"] = self.get_ip('SRC',str(line))
                    self.tag_log.remove('SRC')
            else:
                register["S_IP"] = '-'

            if (re.compile('DST')).search(tag_str):
                if self.tag_log.index('DST') > 0:
                    register["D_IP"] = self.get_ip('DST',str(line))
                    self.tag_log.remove('DST')
            else:
                register["D_IP"] = '-'

            if (re.compile('SPT')).search(tag_str):
                if self.tag_log.index('SPT') > 0:
                    register["S_PORT"] =  self.get_port('SPT',str(line))
                    self.tag_log.remove('SPT')
            else:
                register["S_PORT"] =  '-'

            if (re.compile('DPT')).search(tag_str):
                if self.tag_log.index('DPT') > 0:
                    register["D_PORT"] =  self.get_port('DPT',str(line))
                    self.tag_log.remove('DPT')
            else:
                register["D_PORT"] = '-'

            if (re.compile('PROTO')).search(tag_str):
                if self.tag_log.index('PROTO') > 0:
                    register["Protocol"] =  self.regexp('PROTO',str(line))
                    self.tag_log.remove('PROTO')
            else:
                register["Protocol"] =  '-'

            if (re.compile('MAC')).search(tag_str):
                if self.tag_log.index('MAC') > 0:
                    register["S_MAC"] =  self.regexp('MAC',str(line))
                    register["D_MAC"] =  self.regexp('MAC',str(line))
                    self.tag_log.remove('MAC')
            else:
                register["S_MAC"] = '-'
                register["D_MAC"] = '-'

            try:
                register["S_IP_ID"] = self._db_.query("select ID_IP from ips where Hostname = '"+"".join(register["S_IP"])+"'")[0][0]
            except Exception as ex:
                print "S_IP_ID Exception -> ", ex
                register["S_IP_ID"] = '-'

            try:
                register["D_IP_ID"] = self._db_.query("select ID_IP from ips where Hostname = '"+"".join(register["D_IP"])+"'")[0][0]
            except Exception as ex:
                print "D_IP_ID Exception -> ", ex
                register["D_IP_ID"] = '-'

            register["Info_RAW"] = re.sub('\[','',re.sub('\n',''," ".join(line)))
            register["TAG"] = self.get_tag(line)
            #Introducir los datos en una fila de la tabla Process y pasar el id a dicha entrada
            register["Info_Proc"] = self.get_id_process(line)
            register["Info_Source"] = '-'


            rows.insert_value((None,register["Timestamp"],register["Timestamp_insert"],register["S_IP"],register["D_IP"],register["S_PORT"],register["D_PORT"],register["Protocol"],register["S_MAC"],register["D_MAC"],register["S_IP_ID"],register["D_IP_ID"],register["Info_RAW"],register["Info_Proc"],register["TAG"]))

            self._db_.insert_row('events',rows)
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

    def get_id_process(self, values):

        rows = RowsDatabase(self._db_.num_columns_table('process'))
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

        self._db_.insert_row('process',rows)

        # Si se vuelve a ejecutar cogerá los ids nuevos y no los ya
        # almacenados en la bd.
        
        id_query = self._db_.query("select ID_process from process where ID_process = (select max(ID_process) from process)")

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
        
        id_ip = self._db_.query("select ID_IP from ips where Hostname = '"+hostname+"'")

        #Aquí lo que hago es comprobar si existe una ip similar en la
        # tabla. Si la hay introduzco en el mismo id el valor, y sino
        # se inserta un nuevo registro de ip en la tabla.
        
        if id_ip:
            rows.insert_value((id_ip[0][0], hostname, aliaslist))
        else:
            rows.insert_value((None, hostname, aliaslist))
        
        self._db_.insert_row('ips',rows)


        return hostname
