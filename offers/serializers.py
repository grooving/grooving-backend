from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Offer
from eventLocation.serializers import EventLocationSerializer


class ListOfferSerializer(serializers.HyperlinkedModelSerializer):

    eventLocation = EventLocationSerializer(read_only=True, many=False)

    class Meta:
        model = Offer
        fields = ('id', 'description', 'status', 'date', 'hours', 'eventLocation')
