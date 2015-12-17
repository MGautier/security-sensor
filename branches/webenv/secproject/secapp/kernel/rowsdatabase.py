#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Moisés Gautier Gómez
# Proyecto fin de carrera - Ing. en Informática
# Universidad de Granada


class RowsDatabase(object):

    """
    Clase que nos sirve para preparar secuencias de datos en una fila
    para una tabla de nuestra base de datos
    """

    def __init__(self, num_columns):
        """
        Constructor de la clase
        """

        self.row_values = []
        self.num_columns = int(num_columns)

    def insert_value(self, values):
        """
        Método que almacena internamente los valores de la fila
        para la tabla que queramos rellenar.
        """
        if len(values) <= self.num_columns:
            self.row_values.append(values)
        else:
            print "Insert_value: El tamaño es superior al número de columnas"


    def get_rows(self):
        """
        Método consultor que devuelve todos los valores de la fila
        para la tabla que queramos rellenar
        """
        return self.row_values

    def get_length(self):
        """
        Método consultor que devuelve la el numero de elementos
        introducidos en el objeto de la clase.
        """

        return len(self.row_values)
