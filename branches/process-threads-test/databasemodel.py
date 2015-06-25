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
        print "Base de datos '%s' creada con éxito" % db_name

    def create_table(self, table_name, table_columns):
        self.create_query = table_columns.list_columns()

        try:
            self.cursor = self.database.cursor()
            self.cursor.execute('''create table %s (%s)''' % (table_name,self.create_query))
            print "Tabla '%s' creada con éxito" % table_name
        except db.Error, e:
            print "create_table :-> %s" % e.args[0]
        finally:
            if self.database:
                self.database.close()


test = DatabaseModel('test')
columns = ColumnsDatabase()
columns.insert_column('col1','varchar(50)')
columns.insert_column('col2','text')
columns.insert_column('col3','integer')
test.create_table('prueba',columns)
