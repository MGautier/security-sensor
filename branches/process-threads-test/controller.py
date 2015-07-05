#!/usr/bin/env python
# -*- coding: utf-8 -*-

from source import Firewall
from databasemodel import DatabaseModel
from datetime import date


# Creamos un objeto del tipo Source y operamos con él

test = Firewall('proyecto_bd', args=(1,), source={'T' : 'Firewall', 'M' : 'iptables', 'P' : 'source.log'})
lista = []
test.start()
#print test.processing()
lista = test.join()

print date.today().year
print lista[0]
