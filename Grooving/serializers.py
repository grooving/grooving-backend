from .models import Artist, Portfolio, ArtisticGender
from rest_framework import serializers


class PortfolioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Portfolio
        fields = ('url', 'artisticName', 'artisticGender')


class ArtisticGenderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ArtisticGender
        fields = ('url', 'name', 'parentGender')


class ArtistSerializer(serializers.HyperlinkedModelSerializer):

    portfolio = PortfolioSerializer(read_only=True)

    class Meta:
        model = Artist
        depth = 1
        fields = ('url', 'photo', 'portfolio')

