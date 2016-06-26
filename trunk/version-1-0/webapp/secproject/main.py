#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Moises Gautier Gomez
# Proyecto fin de carrera - Ing. en Informatica
# Universidad de Granada

import signal
import os
import manager
import re


if __name__ == "__main__":
    
    # Instanciamos la clase Manager para la ejecucion de las distintas fuentes
    manager_obj = manager.Manager()

    # Obtenemos la instancia de la fuente iptables para su ejecucion devuelta por el controlador asociado
    iptables = manager_obj.create_controller('iptables')

    # Si establecemos iptables como un pid independiente tendremos que hacer uso de fork para esto y
    # asi el hilo Main sera sobre el cual se haran los operaciones

    if not iptables.get_child_pid() == iptables.get_parent_pid():
        threads = {'Main thread': iptables.get_parent_pid(), 'Thread-1': iptables.get_child_pid()}
    else:
        threads = {'Main thread': iptables.get_parent_pid()}

    # Bucle para la informacion sobre la fuente y la ejecucion de la misma
    while True:

        data_input = raw_input('> ')

        if data_input == 'exit':
            for pid in threads:
                # Primero matamos al proceso hijo y luego al padre
                # para que el hijo no entre en inanicion
                print "--------------------------------------------------"
                print "Matando al proceso: ", int(threads[pid])
                os.kill(int(threads[pid]), signal.SIGKILL)
            os._exit(0)
        elif data_input == 'commands':
            print "-------------------------------------------------"
            print "info -> Informacion sobre la fuente en ejecucion "
            print "clear -> Limpia la pantalla de informacion "
            print "pids -> Muestra los pids asociados en ejecucion "
            print "kill PID (valor) -> Mata al PID que se introduzca (Si es el padre aborta la ejecucion) "
            print "exit -> Aborta la ejecucion del proceso y lo mata."
            print "--------------------------------------------------"
        elif data_input == 'info':
            iptables.get_info()
        elif data_input == 'clear':
            os.system('clear')
        elif data_input == 'pids':
            for it_thread in threads:
                print " " + it_thread + " --> " + threads[it_thread]
        elif "kill" in data_input:
            print "--------------------------------------------------"
            pid = re.split("\W?", data_input)[1]
            print "Matando al proceso: ", pid
            os.kill(int(pid), signal.SIGKILL)
        else:
            print "--------------------------------------------------"
            print "Opcion " + data_input + " incorrecta (commands para mas informacion)"
            print "--------------------------------------------------"
