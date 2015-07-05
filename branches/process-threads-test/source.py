#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import sys
import re
from pygtail import Pygtail

class Source(threading.Thread):

    def __init__(self, group=None, target=None, name=None,
                 args=(), source=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self._source_ = source
        self.type_source = source['T']
        self.model_source = source['M']
        self.path_source = source['P']
        self.parser = []

        return

    def run(self):

        self.log_file = open(self.path_source, 'r')
        #for self.line in Pygtail(self.path_source):
            #sys.stdout.write(self.line)

        #self.linea = self.linea.strip()


        for self.linea in self.log_file:
            self.parser.append(re.split("\W? ", self.linea))


        #self.resultado = [re.split("(\W?) ", self.entry) for self.entry in self.log_file]
        #print self.resultado[1][1]


        #print "en ejecución con parámetros %s y %s" % (self.args, self._source_)
        return

    def processing(self):

        return self.parser
