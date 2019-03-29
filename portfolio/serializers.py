from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Portfolio, Calendar, ArtisticGender, PortfolioModule, Zone, PaymentPackage, Artist


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        depth = 1
        model = User
        fields = ('first_name', 'last_name')


class ArtistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        depth = 1
        model = Artist
        fields = ('user', 'holder', 'photo')


class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calendar
        fields = ('days',)


class ArtisticGenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtisticGender
        fields = ('id', 'name', 'parentGender')


class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = ('name', 'parentZone')


class PaymentPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentPackage
        fields = ('id', 'description')


class PortfolioModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PortfolioModule
        fields = ('type', 'link')


class PortfolioSerializer(serializers.ModelSerializer):

    calendar_set = CalendarSerializer(read_only=True, many=True)
    artisticGender = ArtisticGenderSerializer(many=True, read_only=True)
    portfoliomodule_set = PortfolioModuleSerializer(many=True, read_only=True)
    zone = ZoneSerializer(read_only=True, many=True)
    paymentpackage_set = PaymentPackageSerializer(read_only=True, many=True)
    artist = ArtistSerializer(read_only=True)

    class Meta:

        model = Portfolio
        fields = ('artisticName', 'banner', 'calendar_set', 'artisticGender', 'portfoliomodule_set', 'zone', 'paymentpackage_set', 'artist')


class ShortPortfolioSerializer(serializers.ModelSerializer):

    artisticGender = ArtisticGenderSerializer(read_only=True, many=True)

    class Meta:

        model = Portfolio
        fields = ('artisticName', 'artisticGender')


