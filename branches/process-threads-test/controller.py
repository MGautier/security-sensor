#!/usr/bin/env python
# -*- coding: utf-8 -*-

from source import Source
import databasemodel


# Creamos un objeto del tipo Source y operamos con él

test = Source(args=(1,), source={'T' : 'Firewall', 'M' : 'iptables', 'P' : 'source.log'})
test.start()
print test.processing()
