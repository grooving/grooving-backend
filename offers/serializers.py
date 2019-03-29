from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Offer, PaymentPackage, Customer,Zone, EventLocation, UserAbstract
from eventLocation.serializers import ZoneSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        depth = 1
        model = User
        fields = ('first_name', 'last_name')


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        depth = 1
        model = Customer
        fields = ('user', 'holder', 'photo')


class EventLocationSerializer(serializers.ModelSerializer):
    zone = ZoneSerializer(read_only=True)
    zone_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Zone.objects.all(),
                                                           source='zone')
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = EventLocation
        fields = ('id', 'name', 'address', 'equipment', 'description', 'zone', 'zone_id', 'customer')


class ListOfferSerializer(serializers.HyperlinkedModelSerializer):

    eventLocation = EventLocationSerializer(read_only=True, many=False)

    class Meta:
        model = Offer
        fields = ('id', 'description', 'status', 'price', 'date', 'hours', 'eventLocation')