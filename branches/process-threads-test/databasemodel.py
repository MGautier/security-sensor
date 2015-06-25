#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as db
import sys
from columnsdatabase import ColumnsDatabase


class DatabaseModel(object):
    """
    Clase para la manipulacion de la base de datos. Será cómo un modelo en MVC, en dónde
    nos olvidamos de la capa de datos y simplemente operamos con ellos.
    """
    def __init__(self, db_name):
        """Crea una base de datos con el nombre db_name. Si no existe, la crea."""
        self.database = db.connect(db_name +'.db')
        print "Base de datos %s creada" % db_name

    def create_table(self, table_name, table_columns):
        self.listing = table_columns.list_columns()
        print self.listing
        self.test_listing = [('col1 varchar(50)'),('col2 text')]
        with self.database:
            self.cursor = self.database.cursor()
            self.cursor.execute("create table %s (%s)" % (table_name, self.test_listing))
            #self.cursor.execute("create table %s (%s)" % (table_name,table_columns.list_columns()))


test = DatabaseModel('test')
columns = ColumnsDatabase()
columns.insert_column('col1','varchar(50)')
columns.insert_column('col2','text')
test.create_table('prueba',columns)
