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
import subprocess

# Creamos un objeto del tipo Source y operamos con él

class Controller(object):

    source = ""
    id_thread = []
    args = ()
    source_info = {}
    parent_pid = str(os.getpid())
    child_pid = str(os.getpid())
    name_thread = ""

    def get_source(self):
        return self.source

    def get_parent_pid(self):
        return self.parent_pid

    def get_child_pid(self):
        return self.child_pid

    def get_configuration(self):
        return self.source_info['C']

    def get_type_source(self):
        return self.source_info['T']

    def get_model_source(self):
        return self.source_info['M']

    def get_log_processing(self):
        return self.source_info['P']

    def get_source_info(self):
        return self.source_info

    def get_info(self):
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

    def set_source_info(source_info):
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
        set = {}

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
                if not source_info['P'] == path_source:
                    if not path_source:
                        set['P'] = path_source
                else:
                    set['P'] = source_info['P']

            elif choose == str(2):
                print "--------------------------------------------------"
                config_source = str(raw_input('Archivo de configuración fuente Ejemplo(./kernel/conf/iptables-conf.conf): '))
                print "--------------------------------------------------"
                if not source_info['C'] == config_source:
                    if not config_source:
                        set['C'] = config_source
                else:
                    set['C'] = source_info['C']

            elif choose == str(3):
                if not path_source and not config_source:
                    return source_info
                else:
                    set = {
                        'T': source_info['T'],
                        'M': source_info['M'],
                        'P': path_source,
                        'C': config_source
                    }
            elif choose:
                pass

        return set


    # Si hago uso del fork da el error del Runtime y ejecuta otro pid igual a este
    # si comento el fork funciona correctamente pero al finalizar este proceso Main
    # finaliza toda la ejecucion de procesamiento


    #child_pid = os.fork()
    source = "iptables"
    source_info = {'T': 'Firewall',
                   'M': 'iptables',
                   'P': '/var/log/iptables.log',
                   'C': './kernel/conf/iptables-conf.conf'}
    args = (1,)
    settings = set_source_info(source_info)

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
    source = "snort"

class GlancesController(Controller):
    source = "glances"
