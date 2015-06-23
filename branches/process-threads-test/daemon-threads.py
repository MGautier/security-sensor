#!/usr/bin/env python

import threading

import logging

import time

logging.basicConfig( level=logging.DEBUG,
                     format='[%(levelname)s] - %(threadName)-10s : %(message)s')

def daemon():
    logging.debug('Lanzado')
    time.sleep(2)
    logging.debug('Deteniendo')

d = threading.Thread(target=daemon, name='Daemon')

d.setDaemon(True)

d.start()
d.join() #Nos permite visualizar que el hilo ha terminado, sino saldría sin nuestro control
