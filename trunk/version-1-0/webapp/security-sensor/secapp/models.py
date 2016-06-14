from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


# Author: Moises Gautier Gomez
# Proyecto fin de carrera - Ing. en Informatica
# Universidad de Granada

# Clase que alberga los campos de las IPs extraidas de log

class Ips(models.Model):
    Ip = models.CharField(max_length=60, default='-')
    Hostname = models.CharField(max_length=60, default='-')
    Tag = models.CharField(max_length=255, default='-')

    def __str__(self):
        return '%s' % self.Ip


# Clase que alberga los campos de las fuentes (sources) de seguridad a procesar, en el caso que sigue, Iptables

class LogSources(models.Model):
    Description = models.TextField()
    Type = models.CharField(max_length=100, default='-')
    Model = models.CharField(max_length=255, default='-')
    Active = models.SmallIntegerField()
    Software_Class = models.CharField(max_length=50, default='-')
    Path = models.CharField(max_length=20, default='-')

    def __str__(self):
        return '%s %s ' % (self.Type, self.Description)


# Clase que alberga los campos de los eventos (lineas de log) de una fuente (source) de seguridad procesada

class Events(models.Model):
    Timestamp = models.DateTimeField('Log process date')
    Timestamp_Insertion = models.DateTimeField('Insertion bd date')
    ID_Source = models.ForeignKey(LogSources, on_delete=models.CASCADE)
    Comment = models.TextField()

    def __str__(self):
        return '%s %s %s' % (timezone.localtime(self.Timestamp), self.ID_Source, self.Comment)


# Clase que alberga los campos de los eventos importantes para la visualizacion grafica de los mismos en la vista

class Visualizations(models.Model):

    Week_Month = models.IntegerField('Position of the week in a list. For calendar objects list')
    Week_Day = models.IntegerField('Position of the day in a list. For calendar objects list')
    Name_Day = models.CharField(max_length=25, default='-')
    Date = models.DateField('Events process date')  # Como parametro de entrada recibe objetos datetime.date
    Hour = models.IntegerField('Events process hour')
    ID_Source = models.ForeignKey(LogSources, on_delete=models.CASCADE, blank=True, null=True, related_name="LogSource")
    # Hour: Como parametro de entrada recibe objetos datetime.time, que contendran el valor de la hora en la que
    # se han producido todos esos eventos (sin contar minutos, segundos y microsegundos)
    Process_Events = models.IntegerField('Number of process events in a hour')

    def __str__(self):
        return '%s %s Hora: %s' % (self.Date, self.Name_Day, self.Hour)


# Clase que alberga los campos de los puertos extraidos del log. Tiene dos clases heredadas TCP y UDP

class Ports(models.Model):
    Tag = models.CharField(max_length=25, default='-')

    def __str__(self):
        return '%s' % self.id


# Clase que alberga los campos de un puerto para un determinado tipo de trafico TCP

class Tcp(models.Model):
    id = models.OneToOneField(Ports, on_delete=models.CASCADE, primary_key=True)
    Service = models.CharField(max_length=60, default='-')
    Description = models.CharField(max_length=100, default='-')

    def __str__(self):
        return '%s %s' % (self.id, self.Description)


# Clase que alberga los campos de un puerto para un determinado tipo de trafico UDP

class Udp(models.Model):
    id = models.OneToOneField(Ports, on_delete=models.CASCADE, primary_key=True)
    Service = models.CharField(max_length=60, default='-')
    Description = models.CharField(max_length=100, default='-')

    def __str__(self):
        return '%s %s' % (self.id, self.Description)


# Clase que alberga las etiquetas y su descripcion, para cada paquete procesado en el log

class Tags(models.Model):
    Description = models.TextField()
    Tag = models.CharField(max_length=255, default='-')

    def __str__(self):
        return '%s' % self.Tag


# Clase que alberga los campos MAC extraidos del log

class Macs(models.Model):
    MAC = models.CharField(max_length=17, default='-')
    TAG = models.CharField(max_length=255, default='-')

    def __str__(self):
        return '%s' % self.MAC


# Clase que alberga la informacion relacionada con el paquete extraido mediante el log. La gran mayoria de los campos
# son identificadores o claves foraneas a otros objetos/instancias de la base de datos.

class PacketEventsInformation(models.Model):
    ID_IP_Source = models.ForeignKey(Ips, models.SET_NULL, blank=True, null=True, related_name="ip_source")
    ID_IP_Dest = models.ForeignKey(Ips, models.SET_NULL, blank=True, null=True, related_name="ip_dest")
    ID_Source_Port = models.ForeignKey(Ports, models.SET_NULL, blank=True, null=True, related_name="port_source")
    ID_Dest_Port = models.ForeignKey(Ports, models.SET_NULL, blank=True, null=True, related_name="port_dest")
    Protocol = models.CharField(max_length=20, default='-')
    ID_Source_MAC = models.ForeignKey(Macs, models.SET_NULL, blank=True, null=True, related_name="mac_source")
    ID_Dest_MAC = models.ForeignKey(Macs, models.SET_NULL, blank=True, null=True, related_name="mac_dest")
    RAW_Info = models.TextField(default='-')
    TAG = models.CharField(max_length=255, default='-')
    id = models.OneToOneField(Events, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return '%s' % self.id


# Clase que alberga la informacion relacionada con la informacion adicional de un paquete extraido mediante el log.

class PacketAdditionalInfo(models.Model):
    ID_Tag = models.ForeignKey(Tags, models.SET_NULL, blank=True, null=True, related_name="id_tag")
    ID_Packet_Events = models.ForeignKey(PacketEventsInformation, on_delete=models.CASCADE,
                                         related_name="id_packet_events")
    Value = models.CharField(max_length=255, default='-')

    def __str__(self):
        return '%s %s ' % (self.ID_Tag, self.Value)
