from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Zone


class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ('id', 'name', 'parentZone', 'portfolio_set')


class SearchZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ('id', 'name', 'parentZone')
