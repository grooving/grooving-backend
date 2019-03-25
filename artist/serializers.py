from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Artist
from portfolio.serializers import ShortPortfolioSerializer


class ListArtistSerializer(serializers.HyperlinkedModelSerializer):

    portfolio = ShortPortfolioSerializer(read_only=True)

    class Meta:
        model = Artist
        depth = 1
        fields = ('id', 'photo', 'portfolio')