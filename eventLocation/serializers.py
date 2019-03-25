from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import EventLocation, Zone

class ZoneSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Zone
        fields = ('name', 'parentZone')


class EventLocationSerializer(serializers.HyperlinkedModelSerializer):
    zone = ZoneSerializer(read_only=True, many=False)

    class Meta:
        model = EventLocation
        fields = ('name', 'address', 'equipment', 'description', 'zone')

