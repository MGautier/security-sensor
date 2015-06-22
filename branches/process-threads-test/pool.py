from multiprocessing import *
import ctypes

num = Value(ctypes.c_int, 0)

def A():
    global num

    print "mi función concurrente %s" % num.value

    num.value += 1
