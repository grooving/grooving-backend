from rest_framework import serializers
from Grooving.models import Artist, Customer, Portfolio, EventLocation,Offer
from django.contrib.auth.models import User
from django.db import models

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'last_login', 'first_name', 'last_name', 'email')


class PortfolioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portfolio
        fields = ('id', 'artisticName')


class ArtistSerializer(serializers.ModelSerializer):
    numOffers = serializers.SerializerMethodField('give_offers')
    user = UserSerializer(read_only=True)
    portfolio = PortfolioSerializer(read_only=True)

    class Meta:
        model = Artist
        fields = ('id', 'photo', 'phone', 'portfolio', 'user','numOffers')

    @staticmethod
    def give_offers(self):
        numOffers = Offer.objects.filter(paymentPackage__portfolio__artist=self,status='PENDING').count()
        return numOffers

class CustomerSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'photo', 'phone', 'user')


class LoginSerializer(serializers.Serializer):

    def to_representation(self, instance):
        if isinstance(instance, Artist):
            artistSerializer = ArtistSerializer(instance)

            return {

                'artist': artistSerializer.data,
            }
        elif isinstance(instance, Customer):
            customerSerializer = CustomerSerializer(instance)
            return {
                'customer': customerSerializer.data
            }


    class Meta:

        fields = ('user', 'artist', 'customer')
