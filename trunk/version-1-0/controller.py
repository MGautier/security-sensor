#!/usr/bin/env python
# -*- coding: utf-8 -*-

from firewall import Firewall
from datetime import date


# Creamos un objeto del tipo Source y operamos con él

#input_source = {'T': 'Firewall', 'M': 'iptables', 'P' : 'source.log', 
#'Version' : 'v1.4.21', 'Active' : '1', 'Software_class' : 'Firewall', 
#'Path' : '/var/log/iptablesmini.log'}

test = Firewall('proyecto_bd', args=(1,), source={'T' : 'Firewall', 'M' 
: 'iptables', 'P' : './iptablesmini.log'})
#lista = []
test.start()
#print test.processing()
#lista = test.join()

#print date.today().year
#print lista[0]
