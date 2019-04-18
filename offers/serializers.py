from django.contrib.auth.models import User
from rest_framework import serializers
from Grooving.models import Offer, PaymentPackage, Customer,Zone, EventLocation, Artist, Portfolio
from eventLocation.serializers import ZoneSerializer
from rating.serializers import ListRatingSerializer
from portfolio.serializers import PortfolioSerializer


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


class PortfolioOfferSerializer(serializers.HyperlinkedModelSerializer):

    artist = ArtistOfferSerializer(read_only=True)

    class Meta:
        model = Portfolio
        fields = ('artist',)


class OfferPaymentPackageSerializer(serializers.HyperlinkedModelSerializer):

    portfolio = PortfolioOfferSerializer(read_only=True)

    class Meta:
        model = PaymentPackage
        fields = ('portfolio',)


class OfferWithOnlyPaymentPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentPackage
        fields = ('id', 'description', 'performance', 'fare', 'custom', 'currency')


class ListCustomerOffersSerializer(serializers.ModelSerializer):

    eventLocation = EventLocationSerializer(read_only=True, many=False)
    paymentPackage = OfferWithOnlyPaymentPackageSerializer(read_only=True)
    artist = OfferPaymentPackageSerializer(read_only=True, source='paymentPackage.portfolio.artist')
    rating = ListRatingSerializer(read_only=True)

    class Meta:
        depth = 4
        model = Offer
        fields = ('id', 'description', 'status', 'price', 'date', 'hours', 'artist', 'paymentPackage', 'eventLocation',
                  'rating', 'reason')
