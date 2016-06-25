#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Moises Gautier Gomez
# Proyecto fin de carrera - Ing. en Informatica
# Universidad de Granada


from controller import IptablesController

class Manager():
    def __init__(self):
        self.controller_objects = {'iptables': IptablesController}

    def create_controller(self, typ):
        return self.controller_objects[typ]()
