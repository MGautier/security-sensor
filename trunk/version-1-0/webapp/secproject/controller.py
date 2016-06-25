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
    parent_pid = os.getpid()
    child_pid = os.getpid()

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


class IptablesController(Controller):

    source = "iptables"
    # Si hago uso del fork da el error del Runtime y ejecuta otro pid igual a este
    # si comento el fork funciona correctamente pero al finalizar este proceso Main
    # finaliza toda la ejecucion de procesamiento

    #child_pid = os.fork()
    source_info = {'T': 'Firewall', 'M': 'iptables', 'P': '/var/log/iptables.log',
                   'C': './kernel/conf/iptables-conf.conf'}
    args = (1,)
    thread_iptables = Iptables(
        args=(1,),
        source_info = {'T': 'Firewall', 'M': 'iptables', 'P': '/var/log/iptables.log',
                           'C': './kernel/conf/iptables-conf.conf'}
    )
    thread_iptables.start()
    print "HOLA HOLA : ", thread_iptables.getName()


class SnortController(Controller):
    source = "snort"

class GlancesController(Controller):
    source = "glances"
