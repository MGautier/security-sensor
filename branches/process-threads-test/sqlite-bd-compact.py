#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as bd
import sys

# Conexion de base de datos que devuelve la version del SQLite

connection = bd.connect('pfc')

with connection:

    cursor = connection.cursor()
    cursor.execute('select sqlite_version()')

    data = cursor.fetchone()

    print "SQLite version is: %s" % data
