#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Moisés Gautier Gómez
# Proyecto fin de carrera - Ing. en Informática
# Universidad de Granada


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
        # Los tipos a la hora de definir las columnas de la tabla no se comprueba
        # cuando se introducen. Supongo que se comprobarán a la hora de introducir los
        # valores y darán el error. (SQLite es de tipado dinámico)

        # SQLite uses a more general dynamic type system. In SQLite, the datatype of a
        # value is associated with the value itself, not with its container.
        # The dynamic type system of SQLite is backwards compatible with the more
        # common static type systems of other database engines in the sense
        # that SQL statements that work on statically typed databases should work
        # the same way in SQLite. However, the dynamic typing in SQLite allows it
        # to do things which are not possible in traditional rigidly typed databases.

        self.name_column.append(name_column)
        self.type_column.append(type_column)
        print "Insert column ", name_column, " : ", type_column

    def delete_column(self, name_column):
        """Método que permite eliminar la columna previamente introducida"""
        try:
            index = self.name_column.index(name_column)
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
        listing = ""
        if count() > 0:
            for element in self.name_column:
                index = self.name_column.index(element)
                if index + 1 < count():
                    listing += "" + self.name_column[index] + " " + self.type_column[index] + ", "
                else:
                    listing += "" + self.name_column[index] + " " + self.type_column[index]
            return listing
        else:
            return listing


    def count(self):
        """Método consultor que nos devuelve el número de columnas. Si el valor es 0 es que las listas son distintas"""
        if len(self.name_column) == len(self.type_column):
            return len(self.name_column)
        else:
            return 0
