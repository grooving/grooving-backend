from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Offer


class ListOfferSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Offer
        fields = ('id', 'description', 'status', 'date', 'hours')

