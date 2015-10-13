#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import sys
import re
import subprocess
import socket
import time
from datetime import date
from datetime import datetime
from pygtail import Pygtail
from databasemodel import DatabaseModel
from rowsdatabase import RowsDatabase

class Source(threading.Thread):


    def __init__(self, db_name=None, group=None, target=None, name=None,
                 args=(), source=None, verbose=None):
        """
        Constructor de la clase Source.
        """
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)

        return

    def run(self):
        """
        Sobrecarga de metodo run de la clase Thread.
        """
        pass

    def join(self):
        """
        Sobrecarga del método join de la clase Thread.
        Al ser el que engloba los resultados del hilo, a través
        de él devolvemos los valores que necesitamos procesar
        en el controlador.
        """
        pass

    def process(self):
        pass

    def get_log_values(self):
        pass

class Firewall(Source):

    def __init__(self, db_name=None, group=None, target=None, name=None,
                 args=(), source=None, verbose=None):
        Source.__init__(self, db_name=None, group=None, target=None, name=None,
                        args=(), source=None, verbose=None)
        self.args = args
        self._source_ = source
        self.type_source = source['T']
        self.model_source = source['M']
        self.path_source = source['P']
        self.db = db_name

        self.result = []


    def run(self):
        """
        Sobrecarga de metodo run de la clase Thread.
        """

        self.line = []

        #self.log_file = open(self.path_source, 'r')
        for self.line in Pygtail(self.path_source):
            #sys.stdout.write(self.line)

        #for self.line in self.log_file:
            if(self.line.__len__() > 1): # Si es menor o igual que 1 la linea del log está vacía
                self.result.append(re.split("\W? ", self.line))

        #print "en ejecución con parámetros %s y %s" % (self.args, self._source_)
        return

    def get_log_values(self, line):

        insert_db = {} #Diccionario con los valores del log iptables
        rows = RowsDatabase(self._db_.num_columns_table('events'))
        self.day_log = "" + str(date.today().year) + " " + line[0] + " " + line[1] + ""

        insert_db["Timestamp"] = self.day_log + " " + str(line[2])
        insert_db["Timestamp_insert"] = (datetime.now()).strftime("%Y %b %d - %H:%M:%S.%f")

        #ahora = datetime.strptime(''.join(self.insert_db["Timestamp"]), "%Y %b %d %H:%M:%S")
        #despues = datetime.now()
        #print "Ahora: ", ahora
        #print "Despues: ", despues
        #print ahora > despues
        
        insert_db["S_IP"] = self.get_ip('SRC',str(line))
        insert_db["D_IP"] = self.get_ip('DST',str(line))
        insert_db["S_PORT"] =  self.get_port('SPT',str(line))
        insert_db["D_PORT"] =  self.get_port('DPT',str(line))
        insert_db["Protocol"] =  self.regexp('PROTO',str(line))
        insert_db["S_MAC"] =  self.regexp('MAC',str(line))
        insert_db["D_MAC"] =  self.regexp('MAC',str(line))
        insert_db["S_IP_ID"] = self._db_.query("select ID_IP from ips where Hostname = '"+"".join(insert_db["S_IP"])+"'")[0][0]
        insert_db["D_IP_ID"] = self._db_.query("select ID_IP from ips where Hostname = '"+"".join(insert_db["D_IP"])+"'")[0][0]

        insert_db["Info_RAW"] = re.sub('\[','',re.sub('\n',''," ".join(line)))
        #Introducir los datos en una fila de la tabla Process y pasar el id a dicha entrada
        insert_db["Info_Proc"] = self.get_id_process(line)
        insert_db["Info_Source"] = '-'
        insert_db["TAG"] = self.get_tag(line)

        rows.insert_value((None,insert_db["Timestamp"],insert_db["Timestamp_insert"],insert_db["S_IP"],insert_db["D_IP"],insert_db["S_PORT"],insert_db["D_PORT"],insert_db["Protocol"],insert_db["S_MAC"],insert_db["D_MAC"],insert_db["S_IP_ID"],insert_db["D_IP_ID"],insert_db["Info_RAW"],insert_db["Info_Proc"],insert_db["TAG"]))

        self._db_.insert_row('events',rows)
        

    def regexp(self, source, values):

        return (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")

    def get_id_process(self, values):

        rows = RowsDatabase(self._db_.num_columns_table('process'))
        str_values = str(values)
        string = " ".join(values)
        info_dict = {}
        info_list = ['IN', 'OUT', 'LEN', 'TOS', 'PREC', 'TTL', 'WINDOW']
        for it in info_list:
            check_value = ((re.compile(it + '=\S+')).search(str_values))

            if check_value:
                info_dict[""+it+""] = (((re.compile(it + '=\S+')).search(str_values)).group(0)).split(it + '=')[1].strip("',")
            else:
                info_dict[""+it+""] = '-'

        if ((re.compile('URGP' + '=\S+')).search(str_values)):
            info_dict["URGP"] = ((((re.compile('URGP' + '=\S+')).search(str_values)).group(0)).split('URGP' + '=')[1].strip("',\\n\']"))
        else:
            info_dict["URGP"] = '-'

        if (re.compile('ID=(.*) PROTO')).search(string):
            info_dict["ID"] = (re.compile('ID=(.*) PROTO')).search(string).group(1)
        else:
            info_dict["ID"] = '-'

        if (re.compile('RES=(.*) URGP')).search(string):
            info_dict["RES"] = (re.compile('RES=(.*) URGP')).search(string).group(1)
        else:
            info_dict["RES"] = '-'

        
        rows.insert_value((None, info_dict["IN"], info_dict["OUT"], info_dict["LEN"], info_dict["TOS"], info_dict["PREC"], info_dict["TTL"], info_dict["ID"], info_dict["WINDOW"], info_dict["RES"], info_dict["URGP"]))

        self._db_.insert_row('process',rows)

        # Si se vuelve a ejecutar cogerá los ids nuevos y no los ya
        # almacenados en la bd.
        
        id_query = self._db_.query("select ID_process from process where ID_process = (select max(ID_process) from process)")

        return id_query[0][0]

    def get_tag(self, values):

        self.string = " ".join(values)

        return (re.compile('MSG=(.*) IN')).search(self.string).group(1)

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

    def input_source(self, description):
        """
        Método
        """
        


    def process(self):
        """
        Método que procesa los datos obtenidos y los
        introduce en la base de datos correspondiente.
        """
        self._db_ = DatabaseModel(self.db)

        self.input_source("description")

        #Ahora toca introducir los campos extraidos de log para iptables
        for self.i in range(self.items_list()):

            self.get_log_values(self.result[self.i])


        self._db_.close_db()

    def items_list(self):
        """
        Método que nos devuelve el número de items que tiene
        la lista, que no, el número de elementos de los que
        se compone cada una de ellas."""

        self.count = 0

        # No se hace distinción si la lista contiene una linea
        # vacía o no. Esa distinción se hará a la hora de extraer
        # la información de cada item.

        for self.aux in self.result:
            self.count += 1

        return self.count

    def join(self):
        """
        Sobrecarga del método join de la clase Thread.
        Al ser el que engloba los resultados del hilo, a través
        de él devolvemos los valores que necesitamos procesar
        en el controlador.
        """
        super(Source, self).join()
        self.process()
        return self.result
