#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3 as db
import sys

class DatabaseModel:
    """
    Clase para la manipulacion de la base de datos. Será cómo un modelo en MVC, en dónde
    nos olvidamos de la capa de datos y simplemente operamos con ellos.
    """
    def __init__(self,db_name):
        """Crea una base de datos con el nombre db_name"""
        self.database = db.connect(db_name,'.db')
        print "Base de datos %s creada" % db_name


example = DatabaseModel('puff')
