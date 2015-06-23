#!/usr/bin/env python

import threading

import logging

import time


logging.basicConfig( level=logging.DEBUG,
                     format='[%(levelname)s] - %(threadName)-10s : %(message)s')

def worker():
    logging.debug('Lanzado')
    time.sleep(2)
    logging.debug('Deteniendo')

w = threading.Thread(target=worker, name='Worker')

w.start()
