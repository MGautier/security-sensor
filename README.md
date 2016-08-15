# Sensor para recopilación y visualización de información de seguridad en nodos de una red #

# README #

# Descripción

El objetivo principal del proyecto es desarrollar un software que permita recopilar y visualizar la información generada por las aplicaciones de monitorización y control de seguridad que se ejecutan en una máquina.

La motivación del mismo surge fruto de la necesidad de monitorizar un red corporativa a través de un mecanismo de gestión automatizada de eventos. Los pasos para la realización de este sistema se han modularizado y dividido en diferentes etapas que se acometarán como un todo dentro del proyecto de investigación **VERITAS** (http://nesg.ugr.es/veritas/) del Network Engineering & Security Group (NESG - http://nesg.ugr.es/) perteneciente al área de Ingeniería Telemática de la Universidad de Granada.

Para esta finalidad será necesario definir los pasos para la obtención de logs de una fuente de seguridad, configurar la instalación para dicha fuente, realizar un sistema de parseo de logs para extraer la información, almacenarla en un sistema persistente (base de datos) y visualizarla mediante una interfaz web en la sonda desplegada.

Por último, para comprobar la efectividad y analizar el funcionamiento de la solución software, se realizaría una demostración en directo con procesamiento real de eventos para la fuente de seguridad cuyo ámbito tiene este proyecto que será Iptables.

# Instalación

## Instalación de Django y VirtualEnv

Primero tenemos que instalarnos un entorno virtual de desarrollo para que nuestra aplicación no modifique nuestros paths internos de Python, o si bien queremos que todo lo que nos instalemos sea de uso general no tendríamos que hacer este paso. Para ello vamos a la página oficial del proyecto [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) y seguimos los puntos de instalación que nos indican.

Una vez configurado e instalado el paquete VirtualEnv en nuestra máquina, pasamos a utilizarlo dentro de nuestro proyecto base. Para ello simplemente, una vez clonado el mismo, vamos a la ruta `trunk/version-1-0/webapp/` y ejecutamos lo siguiente:
```bash
$ virtualenv .
$ . bin/activate
```

Una vez dispuesto nuestro entorno virtual vamos a instalar las dependencias necesarias para el funcionamiento de la aplicación. Para este paso es necesario tener instalado el paquete [pip](https://pip.pypa.io/en/stable/installing/), que es el gestor de paquetes del lenguaje Python.

```bash
    $ pip install -U pip
    $ pip install -r requirements.txt
```

Ahora es el momento de configurar nuestro proyecto Django para su ejecución:

```bash
    $ cd secproject
    $ ./manage.py makemigrations
    $ ./manage.py migrate
    $ ./manage.py createsuperuser #Esto nos crea el superuser de administracion
```

Si queremos especificar un usuario distinto a uno general para diferenciar entre entornos de desarrollo y producción, tendremos que acceder a la dirección [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin), ingresar con el super usuario y definir nuevos usuarios para nuestra aplicación. Para nuestro propósito se ha definido un usuario llamado _pfc_ para la parte de desarrollo de la aplicación. Una vez finalizada esta se podrá establecer para un usuario normal o para otro específico.

## Rsyslog

Ya tenemos configurado nuestro entorno de desarrollo de Django, ahora tenemos que configurar los servicios internos de la máquina para que correlen la información generada por iptables en nuestro caso. Así pues, vamos a configurar rsyslog para que redirija los eventos de iptables a `/var/log/iptables.log`.

Incluímos las siguientes líneas en el archivo `/etc/rsyslog.conf`:

```
    # IPTABLES

    :msg,contains,"IPTMSG= " -/var/log/iptables.log
    :msg,regex,"^[ [0-9].[0-9]*] IPTMSG= " -/var/log/iptables.log
    :msg,contains,"IPTMSG= " ~
```

Damos la tupla de permios `0644` a la creación de archivos:

```
   $FileCreateMode 0644
```

Para obtener timestamps más precisos tenemos que comentar la siguiente línea dentro del archivo de configuración de rsyslog:

```
    #$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
```

## LogRotate

Ahora tenemos que configurar el servicio LogRotate para que una vez finalizado el día, los archivos de logs antiguos, los comprima y los almacene en `/var/log/`. Para ello vamos a la ruta `/etc/logrotate.d/` y creamos el archivo `iptables` con el siguiente contenido:

```
    /var/log/iptables.log
    {
      rotate 7
      daily
      missingok
      notifempty
      delaycompress
      compress
      postrotate
      invoke-rc.d rsyslog restart > /dev/null
      endscript
    }
```

## iptables.log

Tenemos que crear un archivo llamado `iptables.log` en `/var/log` con las siguientes características:

```bash
    -rw-r--r-- 1 root adm 15604061 oct 26 20:28 /var/log/iptables.log
    $ chmod 644
    $ chown root:admin
```

## Archivo offset paquete PygTail

El paquete PygTail para la lectura de logs dentro de nuestro sistema se basa en un archivo `.offset` del que consultará información relacionada del archivo del cual queremos obtener el texto correspondiente. Cómo por defecto, éste no puede ejecutarse con privilegios de super usuario dentro de la ruta `/var/log` o hacemos que nuestra aplicación corra directamente sobre super usuario (opción desaconsejada) o creamos el siguiente archivo para cada log que queramos procesar mediante PygTail.

```bash
    -rw-r--rw- 1 root root    13 may  9 20:24 /var/log/iptables.log.offset
    $ chmod 646
    $ chown root:root
```

## Rsyslog.d

Tenemos que decirle al demonio de Rsyslog que todo lo que contenga el mensaje `IPTMSG` (que será nuestro mensaje prefijo para cada paquete obtenido mediante Iptables) lo mande a `/var/log/itpables.log`. Para ello vamos a `/etc/rsyslog.d/iptables.conf` e introducimos lo siguiente:

```bash
    # into separate file and stop their further processing
    if  ($syslogfacility-text == 'kern') and \\
    ($msg contains 'IPTMSG=' and $msg contains 'IN=') \\
    then    -/var/log/iptables.log
        &   ~
```

## Iptables

Los pasos anteriores es para la recolección de eventos generados por Iptables dentro de nuestra máquina. Obviamente habrá que definir unas reglas de filtrado en Iptables cuyo campo de mensaje contenga el siguiente clave/prefijo `IPTMSG= ` (incluir un espacio al final del mensaje). Aquí un ejemplo de las reglas que se han usado para la generación de eventos Iptables:

```bash
    # Generated by iptables-save v1.4.21 on Mon Jan 25 20:37:18 2016
    *filter
    :INPUT ACCEPT [0:0]
    :FORWARD ACCEPT [0:0]
    :OUTPUT ACCEPT [0:0]
    -A INPUT -d 127.0.0.1/32 -p icmp -m icmp --icmp-type 8 -m state --state NEW,RELATED,ESTABLISHED -j LOG --log-prefix "IPTMSG=Connection ICMP "
    -A INPUT -d 127.0.0.1/32 -p icmp -m icmp --icmp-type 8 -m state --state NEW,RELATED,ESTABLISHED -j DROP
    -A INPUT -p tcp -m tcp --dport 22 -j LOG --log-prefix "IPTMSG=Connection SSH "
    -A INPUT -p tcp -m tcp --dport 22 -j DROP
    COMMIT
```

## Web Server

Ahora ya sólo nos queda configurar nuestro servidor web, que en este caso será Nginx. **Importante:** Previamente no debe haberse instalado una versión de servidor web Apache, sino habrá que desinstalar todo y aún así dará muchos problemas. Por lo que es altamente recomendable que la instalación este limpia del paquete apache en cualquiera de sus versiones.

### Nginx

Instalación de Nginx:

```bash
    $ sudo apt-get install nginx
```

Configuración de Nginx:

1. Vamos a la carpeta `/etc/nginx/sites-available/` y creamos nuestro archivo de configuración `myproject.conf` con el siguiente contenido:
```bash
    server {

root /var/www/html;

        # Tipos de archivos index de nuestro sistema

        index index.html index.htm index.nginx-debian.html;

        # Nombre del servidor en local

        server_name localhost;

        location /static/ {
          alias <ruta-descarga-proyecto>/securityproject/trunk/ \\
                 version-1-0/webapp/secproject/secapp/static/;
          expires 30d;
        }

        location / {
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header Host $http_host;
          proxy_redirect off;
          proxy_pass http://127.0.0.1:8000;
          proxy_pass_header Server;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_connect_timeout 10;
          proxy_read_timeout 10;


        }
      }
```
2. Una vez hemos escrito el archivo de configuración hacemos un enlace simbólico del mismo a otra carpeta de nginx, en este caso a ``sites-enabled/''
```bash
    $ sudo ln -s /etc/nginx/sites-available/myproject.conf /etc/nginx/sites-enabled/
```
3. Para comprobar que los archivos de configuración no tienen errores, ejecutamos el siguiente comando y si es éxito, reiniciamos el servicio:
```bash
    $ sudo nginx -t
    $ sudo service nginx restart
```
4. Ahora nos vamos al proyecto Django y lanzamos la instancia:
```bash
    $ ./manage.py runserver
```

Si la configuración se ha realizado correctamente, los contenidos estáticos de la web se verán en el navegador y no tendremos que entrar por el puerto 8000 sino por la dirección de loopback directamente: [http://127.0.0.1/secapp](http://127.0.0.1/secapp) ó [http://127.0.0.1/admin](http://127.0.0.1/admin)

# Licencia

The MIT License (MIT)

Copyright (c) 2016 Moisés Gautier Gómez

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Highcharts Licence

The use of visual package javascript, [Highcharts](http://www.highcharts.com/), follows the license Non-Commercial use.

This project is for Non-commercial purpose and following the [Creative Commons Attribution-NonCommercial 3.0 License](https://creativecommons.org/licenses/by-nc/3.0/).
<p align="center"><img src="https://github.com/MGautier/security-sensor/blob/master/by-nd.png"></p>
