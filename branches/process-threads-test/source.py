#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import sys
import re
from datetime import date
from pygtail import Pygtail

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
        self.insert_db = {} #Diccionario con los valores del log iptables

    def run(self):
        """
        Sobrecarga de metodo run de la clase Thread.
        """

        self.line = []

        self.log_file = open(self.path_source, 'r')
        #for self.line in Pygtail(self.path_source):
            #sys.stdout.write(self.line)

        for self.line in self.log_file:
            self.result.append(re.split("\W? ", self.line))

        #print "en ejecución con parámetros %s y %s" % (self.args, self._source_)
        return

    def get_log_values(self):


        for self.j in range(item_list()):
            if(self.result.__len__() > 1): # Si es menor o igual que 1 la linea del log está vacía
                self.day_log = "" + date.today().year + "/" + self.result[self.j][0] + "/" + self.result[self.j][1] + ""
                self.insert_db["Timestamp"] = [self.day_log + " - " + self.result[self.i][2]]
                #self.insert_db["S_IP"] = [((re.compile("SRC=(.*) DST")).search(self.result[self.i])).group(1)]
                self.insert_db["S_IP"] = [self.regexp('SRC',self.result[self.i])]
                self.insert_db["D_IP"] = [self.regexp('DST',self.result[self.i])]
                self.insert_db["S_PORT"] =  [self.regexp('SPT',self.result[self.i])]
                self.insert_db["D_PORT"] =  [self.regexp('DPT',self.result[self.i])]
                self.insert_db["Protocol"] =  [self.regexp('PROTO',self.result[self.i])]
                self.insert_db["S_MAC"] =  [self.regexp('MAC',self.result[self.i])]
                self.insert_db["D_MAC"] =  [self.regexp('MAC',self.result[self.i])]
                #Coger la key para el IP_ID de Sources de la base de datos
                self.insert_db["Info_RAW"] = [self.result[self.i]]
                #Introducir los datos en una fila de la tabla Process y pasar el id a dicha entrada
                #self.insert_db["Info_Proc"] =
                self.insert_db["TAG"] = [self.get_tag(self.result[self.i])]



    def regexp(self, source, values):

        return (((re.compile(source + '=\S+')).search(values)).group(0)).split(source + "=")[1]

    def get_tag(self, values):

        return ((((re.compile("MSG=(.*) IN")).search(values)).group(0)).split("IN")[0]).split("MSG=")[1]

    def process(self):
        """
        Método que procesa los datos obtenidos y los
        introduce en la base de datos correspondiente.
        """
        self._db_ = DatabaseModel(self.db)

        #Ahora toca introducir los campos extraidos de log para iptables
        for self.i in range(item_list()):
            if(self.result.__len__() > 1): # Si es menor o igual que 1 la linea del log está vacía
                self.day_log = "" + date.today().year + "/" + self.result[self.i][0] + "/" + self.result[self.i][1] + ""
                self.timestamp = self.day_log + " - " + self.result[self.i][2]

                self.s_ip = self.result[self.i][10]
                self.d_ip = self.result[self.i][11]

                self.s_port = self.result[self.i][19]
                self.d_port = self.result[self.i][20]

                self.protocol = self.result[self.i][18]

                self.s_mac = self.result[self.i][9]
                self.d_mac = self.result[self.i][9]



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
        return self.result
