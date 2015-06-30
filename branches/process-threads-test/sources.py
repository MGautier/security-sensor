#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Sources(object):

    def __init__(self, value):
        """
        Constructor de la clase
        """

    def __del__(self):
        """
        Destructor de la clase
        """
        print "Destruyendo la instancia de la clase Sources"

    def start_thread(self):
        """
        Método modificador que inicializa el hilo de ejecución para la
        fuente de datos introducida.
        """

    def stop_thread(self):
        """
        Método modificador que finaliza el hilo de ejecución para la
        fuente de datos introducida.
        """

    def restart_thread(self):
        """
        Método modificador que reinicia el hilo de ejecución para la
        fuente de datos introducida.
        """

    def get_data(self):
        """
        Método virtual que implementará cada clase hija que
        herede de esta superclase y que consistirá en obtener
        los datos del source para introducirlos en la bd.
        """
        pass

    def get_type(self):
        """
        Método consultor que permitirá obtener el tipo de source
        que se ha introducido en el sistema.
        """

    def get_model(self):
        """
        Método consultor que permitirá obtener el modelo de source
        que se ha introducido en el sistema.
        """

    def get_path(self):
        """
        Método consultor que permitirá obtener el path del source
        activo que se ha introducido en el sistema.
        """

    def set_type(self, type_name):
        """
        Método modificador que permitirá modificar el tipo del
        source introducido previamente por el usuario.
        """

    def set_model(self, model_name):
        """
        Método modificador que permitirá modificar el modelo del
        source introducido previamente por el usuario.
        """

    def set_path(sefl, path_name):
        """
        Método modificador que permitirá modificar el path del
        source introducido previamente por el usuario.
        """
