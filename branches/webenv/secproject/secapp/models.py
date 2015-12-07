from __future__ import unicode_literals
from django.db import models


class Ips(models.Model):
    Ip = models.CharField(max_length=60)
    Hostname = models.CharField(max_length=60)
    Tag = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.Ip


class Events(models.Model):
    Timestamp = models.CharField(max_length=100)
    Timestamp_Insertion = models.CharField(max_length=100)
    ID_Source = models.IntegerField()
    Comment = models.TextField()

    def __str__(self):
        return '%s %s' % (self.Timestamp, self.ID_Source)


class Ports(models.Model):
    id_port = models.IntegerField()
    Protocol = models.CharField(max_length=10)
    Service = models.CharField(max_length=60)
    Description = models.CharField(max_length=100)
    Tag = models.CharField(max_length=25)

    def __str__(self):
        return '%s %s' % (self.id_port, self.Protocol)


class LogSources(models.Model):
    Description = models.TextField()
    Type = models.CharField(max_length=100)
    Model = models.CharField(max_length=255)
    Active = models.SmallIntegerField()
    Software_Class = models.CharField(max_length=50)
    Path = models.CharField(max_length=20)

    def __str__(self):
        return '%s %s ' % (self.Type, self.Description)


class PacketAdditionalInfo(models.Model):
    ID_Tag = models.CharField(max_length=255)
    Value = models.CharField(max_length=255)

    def __str__(self):
        return '%s %s ' % (self.ID_Tag, self.Value)


class PacketEventsInformation(models.Model):
    ID_IP_Source = models.IntegerField()
    ID_IP_Dest = models.IntegerField()
    ID_Source_Port = models.IntegerField()
    ID_Dest_Port = models.IntegerField()
    Protocol = models.CharField(max_length=20)
    ID_Source_MAC = models.IntegerField()
    ID_Dest_MAC = models.IntegerField()
    RAW_Info = models.TextField()
    TAG = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.id


class Macs(models.Model):
    MAC = models.CharField(max_length=17)
    TAG = models.CharField(max_length=255)

    def __str__(self):
        return '%s' % self.MAC


class Tags(models.Model):
    TAG = models.CharField(max_length=255)
    Description = models.TextField()

    def __str__(self):
        return '%s' % self.TAG


