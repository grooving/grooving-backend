from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Customer
from user.serializers import UserSerializer, ShortUserSerializer
from eventLocation.serializers import EventLocationSerializer, ShortEventLocationSerializer


class CustomerInfoSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(read_only=True)
    eventLocations = EventLocationSerializer(read_only=True, many=True)

    class Meta:
        depth = 1
        model = Customer
        fields = ('id', 'user', 'photo', 'phone', 'iban', 'paypalAccount', 'eventLocations')


class PublicCustomerInfoSerializer(serializers.ModelSerializer):

    user = ShortUserSerializer(read_only=True)
    eventLocations = ShortEventLocationSerializer(read_only=True, many=True)

    class Meta:
        depth = 1
        model = Customer
        fields = ('id', 'user', 'photo', 'eventLocations')
