from rest_framework import serializers
from models import Events
from django.utils import timezone


class DateTimeTZ(serializers.DateTimeField):

    def to_representation(self, value):
        value = timezone.localtime(value)
        return super(DateTimeTZ, self).to_representation(value)


class EventsSerializer(serializers.ModelSerializer):

    Local_Timestamp = DateTimeTZ(source='Timestamp')


    class Meta:
        model = Events