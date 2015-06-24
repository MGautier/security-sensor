#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('pfc')

c = conn.cursor()

# Comprobemos las tablas que dispone la base de datos (sin encriptar)

c.execute("select name from sqlite_master where type = 'table'")
print c.fetchall() #Muestra más de una fila de resultados

# Guardamos los cambios, si es que los hubiera, con commit

conn.commit()

conn.close()

# Log de iptables
# Jun 18 22:10:38 debian kernel: [12982.320129] Intento de conexion SSH:IN=lo OUT= MAC=00:00:00:00:00:00:00:00:00:00:00:00:08:00 SRC=192.168.1.218 DST=192.168.1.218 LEN=52 TOS=0x00 PREC=0x00 TTL=64 ID=35184 DF PROTO=TCP SPT=58801 DPT=22 WINDOW=256 RES=0x00 ACK URGP=0
