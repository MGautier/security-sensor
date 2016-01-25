from rest_framework import serializers
from models import Events


class SecappSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events