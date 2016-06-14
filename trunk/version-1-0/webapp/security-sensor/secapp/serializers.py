from rest_framework import serializers
from models import Events, Visualizations
from django.utils import timezone

# Author: Moises Gautier Gomez
# Proyecto fin de carrera - Ing. en Informatica
# Universidad de Granada


class DateTimeTZ(serializers.DateTimeField):
    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeTZ, self).to_representation(value)


class EventsSerializer(serializers.ModelSerializer):
    Local_Timestamp = DateTimeTZ(source='Timestamp')

    class Meta:
        model = Events


class VisualizationsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visualizations
