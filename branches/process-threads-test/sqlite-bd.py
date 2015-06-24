#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as bd
import sys

# Conexion de base de datos que devuelve la version del SQLite

connection = None

try:
    connection = bd.connect('pfc')

    cursor = connection.cursor()
    cursor.execute('select sqlite_version()')

    data = cursor.fetchone()

    print "SQLite version is: %s" % data

except bd.Error, e:

    print "Error %s:" % e.args[0]
    sys.exit(1)

finally:

    if connection:
        connection.close()
