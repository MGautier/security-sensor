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

    def get_ip(self):
        return self.Ip

    def get_hostname(self):
        return self.Hostname

    def get_tag(self):
        return self.Tag


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

    def get_description(self):
        return self.Description

    def get_type(self):
        return self.Type

    def get_model(self):
        return self.Model

    def get_active(self):
        return self.Active

    def get_software_class(self):
        return self.Software_Class

    def get_path(self):
        return self.Path


# Clase que alberga el historico de eventos totales de la hora actual

class Historic(models.Model):
    ID_Source = models.ForeignKey(LogSources, on_delete=models.CASCADE)
    Timestamp = models.DateTimeField('Log Process date')
    Events = models.IntegerField('Events stored in the system at that timestamp')

    def __str__(self):
        return '%s-%s' % (timezone.localtime(self.Timestamp), self.Events)

    def get_source(self):
        return self.ID_Source

    def get_timestamp(self):
        return self.Timestamp

    def get_events(self):
        return self.Events


# Clase que alberga los campos de los eventos (lineas de log) de una fuente (source) de seguridad procesada

class Events(models.Model):
    Timestamp = models.DateTimeField('Log process date')
    Timestamp_Insertion = models.DateTimeField('Insertion bd date')
    ID_Source = models.ForeignKey(LogSources, on_delete=models.CASCADE)
    Comment = models.TextField()

    def __str__(self):
        return '%s %s %s' % (timezone.localtime(self.Timestamp), self.ID_Source, self.Comment)

    def get_timestamp(self):
        return self.Timestamp

    def get_timestamp_insertion(self):
        return self.Timestamp_Insertion

    def get_source(self):
        return self.ID_Source

    def get_comment(self):
        return self.Comment


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

    def get_week_month(self):
        return self.Week_Month

    def get_week_day(self):
        return self.Week_Day

    def get_name_day(self):
        return self.Name_Day

    def get_date(self):
        return self.Date

    def get_hour(self):
        return self.Hour

    def get_source(self):
        return self.ID_Source

    def get_process_events(self):
        return self.Process_Events


# Clase que alberga los campos de los puertos extraidos del log. Tiene dos clases heredadas TCP y UDP

class Ports(models.Model):
    Tag = models.CharField(max_length=25, default='-')

    def __str__(self):
        return '%s' % self.id

    def get_tag(self):
        return self.Tag


# Clase que alberga los campos de un puerto para un determinado tipo de trafico TCP

class Tcp(models.Model):
    id = models.OneToOneField(Ports, on_delete=models.CASCADE, primary_key=True)
    Service = models.CharField(max_length=60, default='-')
    Description = models.CharField(max_length=100, default='-')

    def __str__(self):
        return '%s %s' % (self.id, self.Description)

    def get_service(self):
        return self.Service

    def get_description(self):
        return self.Description

    def get_id(self):
        return self.id


# Clase que alberga los campos de un puerto para un determinado tipo de trafico UDP

class Udp(models.Model):
    id = models.OneToOneField(Ports, on_delete=models.CASCADE, primary_key=True)
    Service = models.CharField(max_length=60, default='-')
    Description = models.CharField(max_length=100, default='-')

    def __str__(self):
        return '%s %s' % (self.id, self.Description)

    def get_service(self):
        return self.Service

    def get_description(self):
        return self.Description

    def get_id(self):
        return self.id


# Clase que alberga las etiquetas y su descripcion, para cada paquete procesado en el log

class Tags(models.Model):
    Description = models.TextField()
    Tag = models.CharField(max_length=255, default='-')

    def __str__(self):
        return '%s - %s' % (self.Tag, self.Description)

    def get_description(self):
        return self.Description

    def get_tag(self):
        return self.Tag


# Clase que alberga los campos MAC extraidos del log

class Macs(models.Model):
    MAC = models.CharField(max_length=17, default='-')
    TAG = models.CharField(max_length=255, default='-')

    def __str__(self):
        return '%s' % self.MAC

    def get_mac(self):
        return self.MAC

    def get_tag(self):
        return self.TAG


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

    def get_id_ip_source(self):
        return self.ID_IP_Source

    def get_id_ip_dest(self):
        return self.ID_IP_Dest

    def get_id_source_port(self):
        return self.ID_Source_Port

    def get_id_dest_port(self):
        return self.ID_Dest_Port

    def get_protocol(self):
        return self.Protocol

    def get_id_source_mac(self):
        return self.ID_Source_MAC

    def get_id_dest_mac(self):
        return self.ID_Dest_MAC

    def get_raw_info(self):
        return self.RAW_Info

    def get_tag(self):
        return self.TAG

    def get_id(self):
        return self.id


# Clase que alberga la informacion relacionada con la informacion adicional de un paquete extraido mediante el log.

class PacketAdditionalInfo(models.Model):
    ID_Tag = models.ForeignKey(Tags, models.SET_NULL, blank=True, null=True, related_name="id_tag")
    ID_Packet_Events = models.ForeignKey(PacketEventsInformation, on_delete=models.CASCADE,
                                         related_name="id_packet_events")
    Value = models.CharField(max_length=255, default='-')

    def __str__(self):
        return '%s - %s ' % (self.ID_Tag, self.Value)

    def get_id_tag(self):
        return self.ID_Tag

    def get_id_packet_events(self):
        return self.ID_Packet_Events

    def get_value(self):
        return self.Value
