#!/usr/bin/env python
# -*- coding: utf-8 -*-

from iptables import Iptables
from glances import Glances
from datetime import date

# Author: Moisés Gautier Gómez
# Proyecto fin de carrera - Ing. en Informática
# Universidad de Granada

# Creamos un objeto del tipo Source y operamos con él

test = Iptables(args=(1,), source={'T' : 'Firewall', 'M' : 'iptables', 'P' : './iptables.log', 'C' : './conf/iptables_conf.conf'})
test.start()

#test_2 = Glances('bd_project', args=(1,), source={'T' : 'Watchdog', 'M' : 'glances', 'P' : './glances.csv'})
#test_2.start()


