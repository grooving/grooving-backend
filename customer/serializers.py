from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Customer
from user.serializers import UserSerializer
from eventLocation.serializers import EventLocationSerializer


class CustomerInfoSerializer(serializers.HyperlinkedModelSerializer):

    user = UserSerializer(read_only=True)
    eventLocation = EventLocationSerializer(read_only=True, many=True)

    class Meta:
        depth = 1
        model = Customer
        fields = ('id', 'user', 'photo', 'phone', 'iban', 'paypalAccount', 'eventLocation')
