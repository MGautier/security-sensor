#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Moises Gautier Gomez
# Proyecto fin de carrera - Ing. en Informatica
# Universidad de Granada


# Configuracion del ORM de Django para su uso externo a la aplicacion

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "secproject.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

from iptables import Iptables

# Creamos un objeto del tipo Source y operamos con él


class Controller(object):
    """
    Clase Controller para el manejo de las distintas fuentes
    """

    # Nombre de la fuente
    source = ""

    # Argumentos que pasar a la ejecucion de los Thread
    args = ()

    # Informacion de la fuente a la hora de crear su hilo asociado
    source_info = {}

    # PID del proceso padre (en este caso del proceso Main)
    parent_pid = str(os.getpid())

    # PID del proceso hijo (en este caso de la fuente que corresponda)
    child_pid = str(os.getpid())

    # Nombre del Thread segun la nomenclatura generado por threading
    name_thread = ""

    def get_source(self):
        """
        Metodo que nos devuelve el tipo de fuente
        Returns: String con el valor de la fuente procesada

        """
        return self.source

    def get_parent_pid(self):
        """
        Metodo que nos devuelve el pid asociado al hilo principal (Main)
        Returns: String con el valor del PID del hilo principal en ejecucion (Main)

        """
        return self.parent_pid

    def get_child_pid(self):
        """
        Metodo que nos devuelve el pid asociado al hilo hijo (de la fuente procesada)
        Returns: String con el valor del PID del hilo hijo en ejecucion (de la fuente procesada)

        """
        return self.child_pid

    def get_configuration(self):
        """
        Metodo que nos devuelve la ruta del archivo de configuracion de la fuente
        Returns: String con el valor de la ruta del archivo de configuracion de la fuente

        """
        return self.source_info['C']

    def get_type_source(self):
        """
        Metodo que nos devuelve el tipo de la fuente a procesar
        Returns: String con el valor del tipo de la fuente a procesar

        """
        return self.source_info['T']

    def get_model_source(self):
        """
        Metodo que nos devuelve el modelo de la fuente a procesar
        Returns: String con el valor del modelo de la fuente a procesar

        """
        return self.source_info['M']

    def get_log_processing(self):
        """
        Metodo que nos devuelve la ruta del archivo de log para el procesamiento y obtención de eventos
        Returns: String con el valor de la ruta del archivo de log

        """
        return self.source_info['P']

    def get_source_info(self):
        """
        Metodo que nos devuelve toda la informacion previa de la fuente antes de su ejecucion
        Returns: Diccionario con la informacion previa de la fuente antes de su ejecucion

        """
        return self.source_info

    def get_info(self):
        """
        Metodo que nos imprime por salida estandar toda la informacion perteneciente a la fuente
        Returns: None

        """
        print "--------------------------------------------------"
        print "Source --> ", self.get_source()
        print "Parent pid --> ", self.get_parent_pid()
        print "Child pid --> ", self.get_child_pid()
        print "Type source --> ", self.get_type_source()
        print "Model source --> ", self.get_model_source()
        print "Configuration file --> ", self.get_configuration()
        print "Log processing --> ", self.get_log_processing()
        print "Thread name --> ", self.name_thread
        print "--------------------------------------------------"


class IptablesController(Controller):
    """
    Clase IptablesController que hereda el comportamiento de Controller y que se encarga de la ejecucion
    de la clase Iptables para la ejecucion de los eventos asociados.
    """

    def set_source_info(self):
        """
        Metodo interno de la clase IptablesController que sirve para la modificacion de los parametros
        de configuracion previos a la inicializacion del hilo de procesado iptables
        Args:
            self: Diccionario con la informacion previa de configuracion para la ejecucion de iptables

        Returns: Devuelve la configuracion a aplicar sobre la ejecucion de iptables

        """
        print "--------------------------------------------------"
        print "Introduce los parametros de la configuracion de la fuente - iptables"
        print "Valores por defecto ----"
        print "[1] Ruta procesamiento: \'/var/log/iptables.log\',"
        print "[2] Configuración fuente: \'.kernel/conf/iptables-conf.conf\'"
        print "[3] Salir de la configuración"
        print "Si no quieres modificar el campo introduce Intro en la selección"
        print "--------------------------------------------------"

        choose = 0
        path_source = ""
        config_source = ""
        set_config = {}

        while choose != str(3):
            print "--------------------------------------------------"
            choose = str(raw_input('Introduce parámetro a modificar ([3] - Saltar este paso, [0] - Ayuda): '))
            print "--------------------------------------------------"
            if choose == str(0):
                print "--------------------------------------------------"
                print "Introduce los parametros de la configuracion de la fuente - iptables"
                print "Valores por defecto ----"
                print "[1] Ruta procesamiento: \'/var/log/iptables.log\',"
                print "[2] Configuración fuente: \'.kernel/conf/iptables-conf.conf\'"
                print "[3] Salir de la configuración"
                print "--------------------------------------------------"
            elif choose == str(1):
                print "--------------------------------------------------"
                path_source = str(raw_input('Ruta de procesamiento de logs Ejemplo(/var/log/iptables.log): '))
                print "--------------------------------------------------"
                if not self['P'] == path_source:
                    if not path_source:
                        set_config['P'] = path_source
                else:
                    set_config['P'] = self['P']

            elif choose == str(2):
                print "--------------------------------------------------"
                config_source = str(
                    raw_input('Archivo de configuración fuente Ejemplo(./kernel/conf/iptables-conf.conf): '))
                print "--------------------------------------------------"
                if not self['C'] == config_source:
                    if not config_source:
                        set_config['C'] = config_source
                else:
                    set_config['C'] = self['C']

            elif choose == str(3):
                if not path_source and not config_source:
                    return self
                else:
                    set_config = {
                        'T': self['T'],
                        'M': self['M'],
                        'P': path_source,
                        'C': config_source
                    }
            elif choose:
                pass

        return set_config

    # Si hago uso del fork da el error del Runtime y ejecuta otro pid igual a este
    # si comento el fork funciona correctamente pero al finalizar este proceso Main
    # finaliza toda la ejecucion de procesamiento
    # Relacionado con el metodo start() de threading:
    #
    # Start the thread’s activity.
    # It must be called at most once per thread object. It arranges for the object’s run() method to be invoked in a
    # separate thread of control.
    # This method will raise a RuntimeError if called more than once on the same thread object.

    # child_pid = os.fork()

    source = "iptables"
    source_info = {'T': 'Firewall',
                   'M': 'iptables',
                   'P': '/var/log/iptables.log',
                   'C': './kernel/conf/iptables-conf.conf'}
    args = (1,)
    settings = set_source_info(source_info)

    # Solo cambio el archivo de configuracion y el archivo de log dado que para este caso siempre habra valor
    # fijo para el tipo de fuente que es y el modelo al que representa dentro del sistema.
    # Si no se ha modificado nada esta asignacion sera inutil, en caso opuesto se modifica el diccionario

    if not settings == source_info:
        source_info = settings

    try:
        thread_iptables = Iptables(
            args=args,
            source_info=source_info
        )
        thread_iptables.start()
        name_thread = thread_iptables.getName()
    except Exception as ex:
        print "Exception --> ", ex


class SnortController(Controller):
    """
    Clase de ejemplo Snort
    """
    source = "snort"


class GlancesController(Controller):
    """
    Clase de ejemplo Glances
    """
    source = "glances"
