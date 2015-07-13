#!/usr/bin/python



from pygtail import Pygtail
import sys
import time

while True:
	for line in Pygtail("some.log"):
		sys.stdout.write(line)	
		time.sleep(1)
