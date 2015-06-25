#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ColumnsDatabase(object):
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

    def print_columns(self):
        """"Método que nos imprime las columnas introducidas"""
        print 'Name column: ', self.name_column, ' Type column: ',  self.type_column

    def list_columns(self):
        """
        Método consultor con el contenido de las columnas
        introducidas en formato cadena (para insertar en la query)
        """
        self.listing = ""
        if self.count() > 0:
            for self.element in self.name_column:
                self.index = self.name_column.index(self.element)
                if self.index + 1 < self.count():
                    self.listing += "" + self.name_column[self.index] + " " + self.type_column[self.index] + ", "
                else:
                    self.listing += "" + self.name_column[self.index] + " " + self.type_column[self.index]
            return self.listing
        else:
            return self.listing


    def count(self):
        """Método consultor que nos devuelve el número de columnas. Si el valor es 0 es que las listas son distintas"""
        if len(self.name_column) == len(self.type_column):
            return len(self.name_column)
        else:
            return 0

#col = ColumnsDatabase()

#col.insert_column('col1','varchar(80)')
#col.insert_column('col2','text')
#col.insert_column('col3','integer')
#col.list_columns()
#col.delete_column('col1')
#col.delete_column('col4')

#print col.name_column_list()

#print col.type_column_list()

#print col.list_columns()
