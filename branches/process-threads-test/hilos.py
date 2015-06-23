#!/usr/bin/env python

import threading

def worker(count):
    #funcion que realiza el trabajo en el thread
    print 'Muestro el valor %s para el hilo' % count
    return

threads = list()

for i in range(3):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
