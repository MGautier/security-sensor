#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import io

f = open('source.log', 'r')
while True:
    line = ''
    while len(line) == 0 or line[-1] != '\n':
        tail = f.readline()
        if tail == '':
            time.sleep(0.1)          # avoid busy waiting
            # f.seek(0, io.SEEK_CUR) # appears to be unneccessary
            continue
        line += tail
    print line
