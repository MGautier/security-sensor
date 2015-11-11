#!/usr/bin/env python
# -*- coding: utf-8 -*-

from source import Source
import csv

class Glances(Source):

    def processLine(self, line):

        spamreader = csv.reader(line, delimiter=' ', quotechar=',')
        for row in spamreader:
            print ', '.join(row)
