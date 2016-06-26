#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Moises Gautier Gomez
# Proyecto fin de carrera - Ing. en Informatica
# Universidad de Granada


from controller import IptablesController


class Manager:
    """
    Clase Manager que se encarga del lanzamiento de los controladores de las distintas fuentes
    a procesar.
    """

    def __init__(self):
        """
        Metodo constructor de la clase Manager
        Returns: Devuelve una instancia de la clase Manager

        """

        # Diccionario que contendra todas las fuentes para ir llamandolas una por una en ejecucion
        # o poder seleccionar cual lanzar usando el patron factoria a traves de esta clase

        self.controller_objects = {'iptables': IptablesController}

    def create_controller(self, typ):
        """
        Metodo que lanza instancias de los controladores de las fuentes
        Args:
            typ: Nombre o diccionario con las fuentes a ejecutar por el sistema

        Returns: Devuelve la instancia controladora de la fuente a procesar para su uso en el hilo principal

        """
        return self.controller_objects[typ]()
