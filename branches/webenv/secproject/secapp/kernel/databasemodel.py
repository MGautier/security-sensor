#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as db
import sys
from columnsdatabase import ColumnsDatabase
from rowsdatabase import RowsDatabase
from datetime import datetime

# Author: Moisés Gautier Gómez
# Proyecto fin de carrera - Ing. en Informática
# Universidad de Granada


class DatabaseModel(object):
    """
    Clase para la manipulacion de la base de datos. Será cómo un modelo en MVC, en dónde
    nos olvidamos de la capa de datos y simplemente operamos con ellos.
    """

    def __init__(self, db_name):
        """
        Crea una base de datos con el nombre db_name. Si no existe, la crea.
        Por defecto crea las tablas especificadas para el proyecto.
        """
        self.database = db.connect(db_name +'.db')

        with self.database:

            self.cursor = self.database.cursor()

            self.cursor.execute('''pragma foreign_keys=ON''')

            self.cursor.execute('''create table if not exists ips
            (ID INTEGER PRIMARY KEY, IP VARCHAR(60), Hostname VARCHAR(60),
            Tag VARCHAR(255))''')

            self.cursor.execute('''create table if not exists events
            (ID INTEGER PRIMARY KEY ASC, Timestamp VARCHAR(100),
            Timestamp_Insertion VARCHAR(100), ID_Source INTEGER,
            Comment TEXT)''')

            self.cursor.execute('''create table if not exists ports
            (ID_PORT INTEGER, Protocol VARCHAR(10),
            Service VARCHAR(60), Description VARCHAR(100),
            Tag VARCHAR(25), PRIMARY KEY (ID_PORT, Protocol))''')

            self.cursor.execute('''create table if not exists log_sources
            (ID_Log_Sources INTEGER PRIMARY KEY ASC, Description TEXT,
            Type VARCHAR(100), Model VARCHAR(255), Active TINYINT,
            Software_class VARCHAR(50), Path VARCHAR(20))''')

            self.cursor.execute('''create table if not exists packet_additional_info
            (ID_Packet_Event_Info INTEGER, ID_TAG VARCHAR(255), Value VARCHAR(255))''')

            self.cursor.execute('''create table if not exists packet_events_information
            (ID INTEGER PRIMARY KEY ASC, ID_IP_Source INTEGER, ID_IP_Dest INTEGER,
            ID_Source_PORT INTEGER, ID_Dest_PORT INTEGER, Protocol CHARACTER(20),
            ID_Source_MAC INTEGER, ID_Dest_MAC INTEGER, RAW_Info TEXT, TAG VARCHAR(255)
            )''')

            self.cursor.execute('''create table if not exists macs
            (ID INTEGER PRIMARY KEY ASC, MAC VARCHAR(17), TAG VARCHAR(255))''')

            self.cursor.execute('''create table if not exists tags
            (ID INTEGER PRIMARY KEY ASC, TAG VARCHAR(255), Description TEXT)''')

            actual_time = (datetime.now()).strftime("%Y %b %d - %H:%M:%S.%f")
            print "["+actual_time+"] Base de datos '%s' abierta/creada con éxito" % db_name


    def create_table(self, table_name, table_columns):
        """
        Crea una tabla en la base de datos instanciada por el objeto de clase.
        Además, también añade las columnas necesarias en su creación.
        """

        create_query = table_columns.list_columns()

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

        list = []
        try:
            self.cursor = self.database.cursor()
            self.cursor.execute("select name from sqlite_master where type = 'table'")

            for iter in self.cursor.fetchall():
                string = "" + str(self.iter)
                list.append((self.string.replace("(u'", "")).replace("',)", ""))

            return list
        except db.Error, e:
            print "list_tables :-> %s" % e.args
        return list

    def info_tables(self, table_name):
        """
        Método que nos permite visualizar la información de la tabla que queramos
        """
        info = []
        try:
            self.cursor = self.database.cursor()
            self.cursor.execute("pragma table_info('%s')" % table_name)
            info = [(record[1], record[2]) for record in self.cursor.fetchall()]
            
        except db.Error, e:
            print "info_tables :-> %s" % e.args
            
        return info

    def columns_name_tables(self, table_name):
        """
        Método que nos permite visualizar en forma de lista los nombres de las
        columnas de una tabla.
        """
        info = []

        for it in self.info_tables(table_name):
            info.append(it[0])
        
        return info

    def insert_row(self, table_name, values):
        """
        Método para introducir valores en nuestra tabla de la base de datos.
        Ejemplo: INSERT INTO table_name VALUES(values)
        """

        rows_value = self.check_columns_insert(table_name,values.get_rows())

        size_table = self.num_columns_table(table_name) #Numero de columnas de la tabla
        size_insert = ""

        #Numero de valores a introducir en una fila para el comando executemany
        # de la api de sqlite en python
        

        try:
            self.cursor = self.database.cursor()
            while size_table > 0:
                if size_table - 1 != 0:
                    size_insert += "?, "
                else:
                    size_insert += "?"

                size_table -= 1

            
            
            self.cursor.executemany(("insert or replace into " + table_name + " values("+ size_insert +" )"),  rows_value)

            self.database.commit()
            
        except db.Error, e:
            print "insert_row :-> %s" % e.args


    def query(self, query_string):
        """Método que nos permite realizar querys directamente a la
        base de datos para obtener información directa. En este caso,
        para usar selecciones que nos permitan obtener información
        directa antes de introducir nueva (comprobaciones atómicas).
        """
        
        return_values = []
        try:
            self.cursor = self.database.cursor()

            for row in self.cursor.execute(query_string):
                return_values.append(row)
            self.database.commit()
        except db.Error, e:
            print "query : -> %s " % e.args

        return return_values

    def get_row_events(self, values):
        """
        Método que sirve para extraer los campos pertenecientes a la
        tabla events dentro de un conjunto de datos.
        """


    def delete_row(self, table_name, column_id, row_value):
        """
        Método para eliminar una fila de datos de una tabla.
        Ejemplo: DELETE FROM table_name WHERE column_id = row_value
        """

        try:
            self.cursor = self.database.cursor()
            self.cursor.execute('''delete from %s where %s = '%s' ''' % (table_name, column_id, row_value))
            self.database.commit()
            print "Valor %s = '%s' eliminado de la tabla %s" % (column_id, row_value, table_name)
        except db.Error, e:
            print "delete_row :-> %s" % e.args

    def update_row(self, table_name, column_value, row_value, column_id, value_id):
        """
        Método para actualizar una fila de datos de una tabla.
        Ejemplo: UPDATE table_name SET column_value = row_value WHERE column_id = value_id
        """

        try:
            self.cursor = self.database.cursor()
            self.cursor.execute("update prueba set col4 = ? where col1 =?", (row_value, value_id))
            self.database.commit()
            print "Valor %s = %s del campo id %s = %s actualizado" % (column_value, row_value, column_id, value_id)
        except db.Error, e:
            print "update_row :-> %s" % e.args

    def num_columns_table(self, table_name):
        """
        Método consultor que nos devuelve el número de columnas de una tabla.
        Nos es útil a la hora de crear el objeto RowsDatabase.
        """
        return len(self.info_tables(table_name))

    def check_columns_insert(self, table_name, values):
        """
        Método que comprueba si el numero de columnas coincide con el
        de valores a introducir en la fila de la tabla. Si hay discordancia,
        introduce valores empty ' '
        """
        list_checked = []
        aux_list_checked = []

        # Si el numero de columnas es mayor al numero de valores
        # que vamos a introducir, introducimos valores empty ' '
        # por cada columna que falta

        for iterator in values:

            aux_list_checked = iterator

            if aux_list_checked.__len__() < self.num_columns_table(table_name):

                while aux_list_checked.__len__() < self.num_columns_table(table_name):
                    aux_list_checked += ('',)

            list_checked.append(aux_list_checked)

        return list_checked

    def close_db(self):
        """
        Método para cerrar la base de datos para más operaciones.
        """
        self.database.close()

