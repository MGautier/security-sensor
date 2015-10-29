#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from databasemodel import DatabaseModel
from pygtail import Pygtail


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
			for line in Pygtail(self.path_source):
				print "Procesando linea --> " + str(line)
				self.processLine(line)


        self._db_.close_db()

        return

    def processLine(self):
        pass

