#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class ColumnsDatabase:
    """
    Clase que nos facilita la recolección de información para las columnas
    para cada tabla a la hora de crearlas.
    """

    def __init__(self):
        """Constructor de la clase"""
        self.name_column = []
        self.type_column = []

    def insert_column(self, name_column, type_column):
        """Método que permite introducir los datos asociados a cada columna"""
        self.name_column.append(name_column)
        self.type_column.append(type_column)
        print "Insert column ", name_column, " : ", type_column

    def delete_column(self, name_column):
        """Método que permite eliminar la columna previamente introducida"""
        try:
            self.index = self.name_column.index(name_column)
            self.name_column.remove(name_column)
            self.type_column.pop(self.index)
            print "Delete column", name_column, "..."
        except Exception as ex:
            print "delete_column :->", type(ex), '-> ', ex

    def name_column_list(self):
        """Método consultor que nos devuelve la lista de nombres de columnas"""
        return self.name_column

    def type_column_list(self):
        """Método consultor que nos devuevle la lista de los tipos de cada columna"""
        return self.type_column

    def list_columns(self):
        """Método que nos permite ver el contenido de las columnas introducidas"""
        print 'Name column: ', self.name_column, ' Type column: ',  self.type_column

col = ColumnsDatabase()

col.insert_column('col1','varchar(80)')
col.insert_column('col2','text')
col.insert_column('col3','integer')
col.list_columns()
col.delete_column('col1')
col.delete_column('col4')

print col.name_column_list()

print col.type_column_list()
