#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading

class Source(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), source=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, verbose=verbose)
        self.args = args
        self._source_ = source
        self.type_source = source['T']
        self.model_source = source['M']
        self.path_source = source['P']

        return

    def run(self):
        self.key_word = '13:38:26'
        self.log_file = open(self.path_source, 'r')
        for self.line in self.log_file:
            print self.line.split(' ')

        #print "en ejecución con parámetros %s y %s" % (self.args, self._source_)
        return

for i in range(10):
    gth = Source(args=(i,), source={'T' : 'Firewall', 'M' : 'iptables', 'P' : 'source.log'})
    gth.start()
