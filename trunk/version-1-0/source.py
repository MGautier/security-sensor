#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from databasemodel import DatabaseModel
from pygtail import Pygtail

# Author: Moisés Gautier Gómez
# Proyecto fin de carrera - Ing. en Informática
# Universidad de Granada

class Source(threading.Thread):


    def __init__(self, db_name=None, group=None, target=None, name=None,
                 args=(), source=None, verbose=None):
        """
        Constructor de la clase Source.
        """
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)

        self.args = args
        self._source_ = source
        self.tag_log = []

        self.db_name = db_name
        self.type_source = source['T']
        self.model_source = source['M']
        self.path_source = source['P']

        return

    def run(self):
        """
        Sobrecarga de metodo run de la clase Thread.
        """

        self._db_ = DatabaseModel(self.db_name)

        line = []

        while True:

            print "Pulsa intro para comenzar el análisis"
            print "Escribe exit para abortar el programa\n"
            exit = raw_input('')
            if(exit != "exit"):
                for line in Pygtail(self.path_source):
                    if len(line) > 1:
                        print "\n Procesando línea --> " + str(line)
                        self.processLine(line)
            else:
                break
        
        self._db_.close_db()

        return

    def processLine(self):
        """
        Método que heredan las clases hijo que se encarga del procesado
        de la información de las sources
        """
        pass
