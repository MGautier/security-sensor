#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
from pygtail import Pygtail


# Author: Moisés Gautier Gómez
# Proyecto fin de carrera - Ing. en Informática
# Universidad de Granada

class Source(threading.Thread):
    """
    Clase Source de la que heredan todas las fuentes que queramos procesar en nuestra aplicacion
    """

    def __init__(self, group=None, target=None, name=None,
                 args=(), source=None, verbose=None):
        """
        Metodo constructor de la clase Source
        Args:
            group: por defecto su valor es None; reservado para la futura ampliacion de implementacion de la clase
            ThreadGroup
            target: es el objeto invocado por el metodo interno run(), que por defecto es None mientras nadie lo use
            name: es el nombre del hilo. Por defecto, un nombre para un hilo se construye de la forma "Thread-N",
            donde N es un numero entero decimal.
            args: es una tupla de datos usada para la invocacion del target. Por defecto es ()
            source: Diccionario con informacion sobre la fuente a procesar (Nombre, Archivo de configuracion,
            modelo, Archivo de log, etc)
            verbose: None

        Returns: Objeto de la clase Source inicializado que hereda funcionalidad de la clase Thread

        """

        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, verbose=verbose)

        self._source_ = source

        # Tipo de fuente
        self.type_source = source['T']
        # Modelo de fuente
        self.model_source = source['M']
        # Path donde se encuentra el archivo log de la fuente
        self.path_source = source['P']
        # Path donde se encuentra el archivo de configuracion de los parametros del source
        self.config_file = source['C']

        return

    def run(self):
        """
        Sobrecarga de metodo run de la clase Thread. Lanza la ejecución de la hebra principal de la aplicacion
        django.
        """

        # Cargamos la configuracion de los parametros del source para que se pueda obtener informacion
        # de la misma que introducir en la BD a la hora de la carga de valores de logs.

        self.read_config_file()

        # Voy a usar estas variables para llevar el conteo del archivo offset a la hora de modificar
        # su informacion con respecto al archivo .log

        obj = Pygtail(self.path_source)

        while True:
                try:
                    for line in obj:
                        if len(line) > 1:
                            self.process_line(line)
                except Exception as ex:
                    print "Pygtail processing -> ", ex

        return

    @staticmethod
    def read_config_file():
        """
        Método modificador de la clase que abre y lee el contenido del archivo
        de configuracion para el software iptables. El contenido del archivo se
        almacena internamente en los atributos de la clase.
        Returns: None

        """

        pass

    @staticmethod
    def process_line(line):
        """
        Método modificador que procesa e introduce en un bd la informacion
        relevante del filtrado de paquetes, en este caso, de iptables.
        Args:
            line: Objeto file que contiene el log leido de iptables

        Returns: Muestra informacion por linea de comando de los eventos procesados y almacenados en la bd

        """

        pass
