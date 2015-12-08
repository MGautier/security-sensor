from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Ips(models.Model):
    Ip = models.CharField(max_length=60)
    Hostname = models.CharField(max_length=60)
    Tag = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.Ip


class LogSources(models.Model):
    Description = models.TextField()
    Type = models.CharField(max_length=100)
    Model = models.CharField(max_length=255)
    Active = models.SmallIntegerField()
    Software_Class = models.CharField(max_length=50)
    Path = models.CharField(max_length=20)

    def __str__(self):
        return '%s %s ' % (self.Type, self.Description)


class Events(models.Model):
    Timestamp = models.CharField(max_length=100)
    Timestamp_Insertion = models.CharField(max_length=100)
    ID_Source = models.ForeignKey(LogSources, on_delete=models.CASCADE)
    Comment = models.TextField()

    def __str__(self):
        return '%s %s' % (self.Timestamp, self.ID_Source)


class Ports(models.Model):
    id_port = models.IntegerField(primary_key=True)
    Protocol = models.CharField(max_length=10)
    Service = models.CharField(max_length=60)
    Description = models.CharField(max_length=100)
    Tag = models.CharField(max_length=25)

    def __str__(self):
        return '%s %s' % (self.id_port, self.Protocol)


class Tags(models.Model):
    Description = models.TextField()
    Tag = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.Tag


class PacketAdditionalInfo(models.Model):
    ID_Tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
    Value = models.CharField(max_length=255)

    def __str__(self):
        return '%s %s ' % (self.ID_Tag, self.Value)


class Macs(models.Model):
    MAC = models.CharField(max_length=17)
    TAG = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.MAC


class PacketEventsInformation(models.Model):
    ID_IP_Source = models.ForeignKey(Ips, on_delete=models.CASCADE, related_name="ip_source")
    ID_IP_Dest = models.ForeignKey(Ips, on_delete=models.CASCADE, related_name="ip_dest")
    ID_Source_Port = models.ForeignKey(Ports, on_delete=models.CASCADE, related_name="port_source")
    ID_Dest_Port = models.ForeignKey(Ports, on_delete=models.CASCADE, related_name="port_dest")
    Protocol = models.CharField(max_length=20)
    ID_Source_MAC = models.ForeignKey(Macs, on_delete=models.CASCADE, related_name="mac_source")
    ID_Dest_MAC = models.ForeignKey(Macs, on_delete=models.CASCADE, related_name="mac_dest")
    RAW_Info = models.TextField()
    TAG = models.ForeignKey(Tags, on_delete=models.CASCADE, related_name="tags")

    def __str__(self):
        return '%s' % self.id


