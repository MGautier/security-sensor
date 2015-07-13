#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import sys
import re
import socket
from datetime import date
from pygtail import Pygtail
from databasemodel import DatabaseModel

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

        self.log_file = open(self.path_source, 'r')
        #for self.line in Pygtail(self.path_source):
            #sys.stdout.write(self.line)

        for self.line in self.log_file:
            if(self.line.__len__() > 1): # Si es menor o igual que 1 la linea del log está vacía
                self.result.append(re.split("\W? ", self.line))

        #print "en ejecución con parámetros %s y %s" % (self.args, self._source_)
        return

    def get_log_values(self, line):

        self.insert_db = {} #Diccionario con los valores del log iptables

        self.day_log = "" + str(date.today().year) + "/" + line[0] + "/" + line[1] + ""
        self.insert_db["Timestamp"] = [self.day_log + " - " + line[2]]
        self.insert_db["S_IP"] = [self.get_ip('SRC',line)]
        self.insert_db["D_IP"] = [self.get_ip('DST',line)]
        self.insert_db["S_PORT"] =  [self.regexp('SPT',str(line))]
        self.insert_db["D_PORT"] =  [self.regexp('DPT',str(line))]
        self.insert_db["Protocol"] =  [self.regexp('PROTO',str(line))]
        self.insert_db["S_MAC"] =  [self.regexp('MAC',str(line))]
        self.insert_db["D_MAC"] =  [self.regexp('MAC',str(line))]
        #Coger la key para el IP_ID de Sources de la base de datos
        self.insert_db["Info_RAW"] = [re.sub('\[','',re.sub('\n',''," ".join(line)))]
        #Introducir los datos en una fila de la tabla Process y pasar el id a dicha entrada
        #self.insert_db["Info_Proc"] =
        self.insert_db["TAG"] = [self.get_tag(line)]

        return self.insert_db

    def regexp(self, source, values):

        return (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")

    def get_tag(self, values):

        self.string = " ".join(values)

        return (re.compile('MSG=(.*) IN')).search(self.string).group(1)

    def get_ip(self, source, values):

        self.ip_result = (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + '=')[1].strip("',")
        self.rows = RowsDatabase(self._db_.num_columns_table('ips'))
        self.hostname, self.aliaslist, self.ipaddrlist = socket.gethostbyaddr(self.ip_result)
        self.rows.insert_value((self.ip_result, self.hostname, ))
        #ME FALTA ESTA PARTE
        self._db_.insert_row('ips',self.ip_result)


    def process(self):
        """
        Método que procesa los datos obtenidos y los
        introduce en la base de datos correspondiente.
        """
        self._db_ = DatabaseModel(self.db)
        self.dictionary = {}

        #Ahora toca introducir los campos extraidos de log para iptables
        for self.i in range(self.items_list()):

            self.dictionary = self.get_log_values(self.result[self.i])
            print self.dictionary


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
