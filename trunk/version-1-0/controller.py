#!/usr/bin/env python
# -*- coding: utf-8 -*-

from firewall import Firewall
from datetime import date


# Creamos un objeto del tipo Source y operamos con él

test = Firewall('proyecto_bd', args=(1,), source={'T' : 'Firewall', 'M' 
: 'iptables', 'P' : './iptablesmini.log'})
test.start()

