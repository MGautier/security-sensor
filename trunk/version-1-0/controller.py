#!/usr/bin/env python
# -*- coding: utf-8 -*-

from iptables import Iptables
from datetime import date


# Creamos un objeto del tipo Source y operamos con él

test = Iptables('proyecto_bd', args=(1,), source={'T' : 'Firewall', 'M' 
: 'iptables', 'P' : './iptables.log'})
test.start()

