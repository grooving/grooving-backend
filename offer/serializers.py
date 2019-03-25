from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Offer, PaymentPackage, EventLocation
from utils.Assertions import assert_true

'''class OfferSerializer(serializers.Serializer):
    class Meta:
        model = Offer
        fields = '__all__'

    def create(self, validated_data):
        return Offer(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.date = validated_data.get('date', instance.date)
        instance.hours = validated_data.get('hours', instance.hours)
        instance.paymentCode = validated_data.get('paymentCode', instance.paymentCode)
        instance.eventLocation_id = validated_data.get('eventLocation_id', instance.eventLocation_id)
        instance.paymentPackage_id = validated_data.get('paymentPackage_id', instance.paymentPackage_id)
        return instance
'''


class PaymentPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPackage
        fields = ('id', 'description', 'appliedVAT', 'portfolio_id', 'performance_id', 'fare_id', 'custom_id')


class EventLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLocation
        fields = ('id', 'address', 'equipment', 'description')


class OfferSerializer(serializers.ModelSerializer):

    paymentPackage = PaymentPackageSerializer(read_only=True)
    paymentPackage_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PaymentPackage.objects.all(),
                                                           source='paymentPackage')
    eventLocation = EventLocationSerializer(read_only=True)
    eventLocation_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=EventLocation.objects.all(),
                                                          source='eventLocation')

    class Meta:
        model = Offer
        fields = ('id', 'description', 'status', 'date', 'hours', 'price', 'paymentCode', 'paymentPackage',
                  'paymentPackage_id', 'eventLocation', 'eventLocation_id')

    # Esto sobrescrive una función heredada del serializer.
    def save(self):
        if self.initial_data.get('id') is None:
            # creation
            offer = Offer()
            offer = self._service_create(self.initial_data, offer)
        else:
            # edit
            print("Clave primaria:" + str(self.initial_data.get('id')))
            offer = Offer.objects.get(pk=self.initial_data.get('id'))
            offer = self._service_update(self.initial_data, offer)
        offer.save()
        return offer

    # Se pondrá service delante de nuestros métodos para no sobrescribir por error métodos del serializer
    @staticmethod
    def _service_create(json: dict, offer: Offer):
        offer.description = json.get('description')
        offer.date = json.get('date')
        offer.status = 'PENDING'
        offer.paymentCode = None
        offer.eventLocation = EventLocation.objects.get(pk=json.get('eventLocation_id'))
        offer.paymentPackage = PaymentPackage.objects.get(pk=json.get('paymentPackage_id'))
        if offer.paymentPackage.performance is not None:
            offer.hours = offer.paymentPackage.performance.hours
            offer.price = offer.paymentPackage.performance.price
            offer.currency = offer.paymentPackage.performance.currency
        elif offer.paymentPackage.fare is not None:
            offer.price = offer.paymentPackage.fare.priceHour * json['hours']
            offer.currency = offer.paymentPackage.fare.currency
        elif offer.paymentPackage.custom is not None:
            offer.price = json['price']
            offer.currency = offer.paymentPackage.custom.currency
        return offer

    @staticmethod
    def _service_update(json: dict):
        offer_in_db = Offer.objects.filter(pk=json.id).first()
        assert_true(offer_in_db, "No existe una oferta con esa id")
        return json

    def validate(self, data):
        if data.get("description") is None:
            raise serializers.ValidationError("description field not provided")
        if data.get("date") is None:
            raise serializers.ValidationError("date field not provided")
        if data.get("paymentPackage_id") is None:
            raise serializers.ValidationError("paymentPackage_id field not provided")
        if data.get("eventLocation_id") is None:
            raise serializers.ValidationError("eventLocation_id field not provided")
        return True




"""
class CreateOfferRequest(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ('description', 'date', 'hours', 'price', 'paymentPackage_id', 'eventLocation_id')

"""


