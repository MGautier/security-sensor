#!/usr/bin/env python
# -*- coding: utf-8 -*-


class RowsDatabase(object):

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
        if len(values) < self.num_columns:
            self.row_values.append(values)
        else:
            print "Insert_value: El tamaño es superior al número de columnas"


    def get_rows(self):
        """
        Método consultor que devuelve todos los valores de la fila
        para la tabla que queramos rellenar
        """
        return self.row_values
