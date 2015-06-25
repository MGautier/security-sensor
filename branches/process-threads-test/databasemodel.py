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
        """
        Crea una tabla en la base de datos instanciada por el objeto de clase.
        Además, también añade las columnas necesarias en su creación.
        """
        self.create_query = table_columns.list_columns()

        try:
            self.cursor = self.database.cursor()
            self.cursor.execute('''create table %s (%s)''' % (table_name,self.create_query))
            print "Tabla '%s' creada con éxito" % table_name
        except db.Error, e:
            print "create_table :-> %s" % e.args[0]

    def alter_table_name(self, table_name, new_table_name):
        """
        Método que permite modificar el nombre de la tabla. Si hay
        eventos asociados al anterior nombre de tabla, tendrán que
        redefinirse con el nuevo nombre establecido.
        """

        try:
            self.cursor = self.database.cursor()
            if new_table_name != table_name: #Compruebo si se va a renombrar una tabla o no
                self.cursor.execute('''alter table %s rename to %s''' % (table_name, new_table_name))
                print "Tabla '%s' renombrada a '%s' con éxito" % (table_name, new_table_name)
        except db.Error, e:
            print "alter_table_name :-> %s" % e.args[0]

    def alter_table_column(self, table_name, add_column):
        """
        Método que permite añadir una columna a la tabla.
        """

        try:
            self.cursor = self.database.cursor()
            self.cursor.execute('''alter table %s add %s''' % (table_name, add_column.list_columns()))
            print "Columna '%s' añadida a la tabla '%s' con éxito" % (add_column.list_columns(), table_name)
        except db.Error, e:
            print "alter_table_column :-> %s" % e.args[0]

    def close_db(self):
        """
        Método para cerrar la base de datos para más operaciones.
        """
        self.database.close()

test = DatabaseModel('test')
columns = ColumnsDatabase()
columns.insert_column('col1','varchar(50)')
columns.insert_column('col2','text')
columns.insert_column('col3','integer')
test.create_table('prueba',columns)
col = ColumnsDatabase()
col.insert_column('col4','tinyint')
test.alter_table_column('prueba',col)
test.close_db()
