from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Offer, PaymentPackage, Customer,Zone, EventLocation, Artist, Portfolio, Rating
from eventLocation.serializers import ZoneSerializer
from rating.serializers import ListRatingSerializer
from portfolio.serializers import PortfolioSerializer, ArtistSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        depth = 1
        model = User
        fields = ('first_name', 'last_name')


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        depth = 1
        model = Customer
        fields = ('id', 'user', 'photo')


class ArtistOfferSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        depth = 4
        model = Artist
        fields = ('id', 'user', 'photo')


class EventLocationSerializer(serializers.HyperlinkedModelSerializer):
    zone = ZoneSerializer(read_only=True)
    zone_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Zone.objects.all(),
                                                           source='zone')
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = EventLocation
        fields = ('id', 'name', 'address', 'equipment', 'description', 'zone', 'zone_id', 'customer')


class ListArtistOffersSerializer(serializers.HyperlinkedModelSerializer):

    eventLocation = EventLocationSerializer(read_only=True, many=False)

    class Meta:
        model = Offer
        fields = ('id', 'description', 'status', 'price', 'date', 'hours', 'eventLocation', 'reason')


class OfferPaymentPackageSerializer(serializers.HyperlinkedModelSerializer):

    portfolio = PortfolioSerializer(read_only=True)

    class Meta:
        model = PaymentPackage
        fields = ('portfolio',)


class PortfolioOfferSerializer(serializers.HyperlinkedModelSerializer):

    artist = ListArtistOffersSerializer(read_only=True)

    class Meta:
        model = Portfolio
        fields = ('artist',)


class ListCustomerOffersSerializer(serializers.HyperlinkedModelSerializer):

    eventLocation = EventLocationSerializer(read_only=True, many=False)
    paymentPackage = OfferPaymentPackageSerializer(read_only=True, source='paymentPackage.portfolio.artist')
    rating = ListRatingSerializer(read_only=True)

    class Meta:
        depth = 4
        model = Offer
        fields = ('id', 'description', 'status', 'price', 'date', 'hours', 'paymentPackage', 'eventLocation', 'rating', 'reason')
