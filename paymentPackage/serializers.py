from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Portfolio, Calendar, ArtisticGender, PortfolioModule, Zone, PaymentPackage, Custom, Fare, Performance


class CustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Custom
        fields = ('id', 'minimumPrice', 'currency')


class FareSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fare
        fields = ('id', 'priceHour', 'currency')


class PerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Performance
        fields = ('id', 'info', 'hours', 'price', 'currency')


class PaymentPackageSerializer(serializers.ModelSerializer):

    custom = CustomSerializer(read_only=True)
    fare = FareSerializer(read_only=True)
    performance = PerformanceSerializer(read_only=True)
    appliedVAT = serializers.DecimalField(max_digits=5, decimal_places=2, coerce_to_string=True)

    class Meta:
        model = PaymentPackage
        fields = ('id', 'description', 'appliedVAT', 'custom', 'fare', 'performance')

