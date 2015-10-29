#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading


class Source(threading.Thread):


    def __init__(self, db_name=None, group=None, target=None, name=None,
                 args=(), source=None, verbose=None):
        """
        Constructor de la clase Source.
        """
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)

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

        #self.input_source("description") #Sirve esto para algo???


        self.line = []

        self.log_file = open(self.path_source, 'r')
        while True:
			for self.line in Pygtail(self.path_source):
				print "Procesando linea --> " + str(self.line) #sys.stdout.write(self.line)
				self.processLine(self.line)


        self._db_.close_db()

        
        #for self.line in self.log_file:

        #    if(self.line.__len__() > 1): # Si es menor o igual que 1 la linea del log está vacía
        #        self.result.append(re.split("\W? ", self.line))

        #print "en ejecución con parámetros %s y %s" % (self.args, self._source_)
        return

    def process(self):
        pass

    def processLine(self):
        pass

