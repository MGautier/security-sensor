#!/bin/bash

while true
do
    # Muestra la hora actual por salida estandar
    echo `date`
    # Muestra el error por stderr
    echo 'error!' >&2
    sleep 1
done
