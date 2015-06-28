#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as db
import sys
from columnsdatabase import ColumnsDatabase
from rowsdatabase import RowsDatabase


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
            self.cursor.execute('''create table if not exists %s (%s)''' % (table_name,self.create_query))
            self.database.commit()
            print "Tabla '%s' creada con éxito" % table_name
        except db.Error, e:
            print "create_table :-> %s" % e.args

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
                self.database.commit()
                print "Tabla '%s' renombrada a '%s' con éxito" % (table_name, new_table_name)
        except db.Error, e:
            print "alter_table_name :-> %s" % e.args

    def alter_table_column(self, table_name, add_column):
        """
        Método que permite añadir una columna a la tabla.
        """

        try:
            self.cursor = self.database.cursor()
            self.cursor.execute('''alter table %s add %s''' % (table_name, add_column.list_columns()))
            self.database.commit()
            print "Columna '%s' añadida a la tabla '%s' con éxito" % (add_column.list_columns(), table_name)
        except db.Error, e:
            print "alter_table_column :-> %s" % e.args

    def drop_table(self, table_name):
        """
        Método que permite eliminar una tabla de la base de datos.
        """
        try:
            self.cursor = self.database.cursor()
            self.cursor.execute('''drop table if exists %s''' % (table_name))
            self.database.commit()
            print "Tabla '%s' eliminada con éxito" % (table_name)
        except db.Error, e:
            print "drop_table :-> %s" % e.args

    def list_tables(self):
        """
        Método que permite listar todas las tablas de la base de datos.
        """

        self.list = []
        try:
            self.cursor = self.database.cursor()
            self.cursor.execute("select name from sqlite_master where type = 'table'")

            for self.iter in self.cursor.fetchall():
                self.aux_string = "" + str(self.iter)
                self.list.append((self.aux_string.replace("(u'", "")).replace("',)", ""))

            return self.list
        except db.Error, e:
            print "list_tables :-> %s" % e.args
        return self.list

    def info_tables(self, table_name):
        """
        Método que nos permite visualizar la información de la tabla que queramos
        """
        self.info = []
        try:
            self.cursor = self.database.cursor()
            self.cursor.execute("pragma table_info('%s')" % table_name)
            self.info = [(self.record[1], self.record[2]) for self.record in self.cursor.fetchall()]
            return self.info
        except db.Error, e:
            print "info_tables :-> %s" % e.args
            return self.info

    def insert_row(self, table_name, rows_value):
        """
        Método para introducir valores en nuestra tabla de la base de datos.
        """
        self.rows_value = rows_value.get_rows()

        try:
            self.cursor = self.database.cursor()
            self.cursor.executemany("insert into '%s' values(?)" % (table_name, rows_value))
            self.database.commit()
            print "Valores introducidos en la tabla %s" % table_name
        except db.Error, e:
            print "insert_row :->" % (table_name)

    def num_columns_table(self, table_name):
        """
        Método consultor que nos devuelve el número de columnas de una tabla.
        Nos es útil a la hora de crear el objeto RowsDatabase.
        """
        return len(self.info_tables(table_name))

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
test.create_table('ejemplo',columns)
#print test.num_columns_table('prueba')
col = ColumnsDatabase()
col.insert_column('col4','tinyint')
test.alter_table_column('prueba',col)
print test.list_tables()[0]
print test.info_tables('prueba')
rows = RowsDatabase(int(test.num_columns_table('prueba')))
rows.insert_value(('fila1','más texto',200))
rows.insert_value(('fila2','menos texto',160))
test.insert_row('prueba', rows)
test.close_db()
