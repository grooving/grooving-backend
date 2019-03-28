from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import Offer, PaymentPackage, EventLocation, Customer
from utils.Assertions import assert_true
from django.db import IntegrityError
import random
import string

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
    def save(self, pk=None):
        if self.initial_data.get('id') is None and pk is None:
            # creation
            offer = Offer()
            offer = self._service_create(self.initial_data, offer)
        else:
            # edit
            id = (self.initial_data, pk)[pk is not None]

            offer = Offer.objects.filter(pk=id).first()
            offer = self._service_update(self.initial_data, offer)

        return offer

    @staticmethod
    def service_made_payment_artist(paymentCode):
        offer = Offer.objects.filter(paymentCode=paymentCode).first()
        assert_true(offer, 'La oferta no existe')
        assert_true(offer.status == 'CONTRACT_MADE', 'Posiblemente el pago ya se ha hecho')

        offer.status = 'PAYMENT_MADE'
        #try:
            #TODO: Pago por braintree
        #except:
            #offer.status == 'CONTRACT_MADE'
        offer.save()

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
        offer.save()
        return offer

    def _service_update(self, json: dict, offer_in_db: Offer):
        assert_true(offer_in_db, "No existe una oferta con esa id")
        offer = self._service_update_status(json, offer_in_db)

        return offer

    def _service_update_status(self, json: dict, offer_in_db: Offer):
        json_status = json.get('status')
        if json_status:
            status_in_db = offer_in_db.status
            normal_transitions = {'PENDING': 'CONTRACT_MADE'}

            #TODO: Must be check the login
            customer_flowstop_transitions={'PENDING': 'WITHDRAWN',
                                           'NEGOTIATION': 'WITHDRAWN', 'CONTRACT_MADE': 'WITHDRAWN'}

            artist_flowstop_transitions={'PENDING': 'REJECTED',
                                         'NEGOTIATION': 'REJECTED', 'CONTRACT_MADE': 'CANCELED'}

            allowed_transition = (normal_transitions.get(status_in_db) == json_status
                                  or artist_flowstop_transitions.get(status_in_db) == json_status
                                  or customer_flowstop_transitions.get(status_in_db) == json_status
                                  or status_in_db == json_status
                                  )

            assert_true(allowed_transition, "Not allowed status transition: " + status_in_db + " to "
                        + json_status + ".")

            if json_status == "CONTRACT_MADE":
                while True:
                    # noinspection PyBroadException
                    try:
                        offer_in_db.paymentCode = self._service_generate_unique_payment_code()
                        offer_in_db.save()
                        break
                    except IntegrityError:
                        continue

            print("ESTADO DB ANTES:" + offer_in_db.status)
            offer_in_db.status = json_status
            offer_in_db.save()
            print("ESTADO DB DESPUES:" + offer_in_db.status)
            return offer_in_db

    @staticmethod
    def _service_generate_unique_payment_code():
        random_alphanumeric = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        payment_code = random_alphanumeric
        return payment_code

    def validate(self, request):
        customer = Customer.objects.filter(user_id=request.user.id).first()
        if customer is None:
            raise serializers.ValidationError("user isn't authorized")
        json = request.data
        if json.get("description") is None:
            raise serializers.ValidationError("description field not provided")
        if json.get("date") is None:
            raise serializers.ValidationError("date field not provided")
        if json.get("paymentPackage_id") is None:
            raise serializers.ValidationError("paymentPackage_id field not provided")
        paymentPackage = PaymentPackage.objects.filter(pk=json.get("paymentPackage_id")).first()
        if paymentPackage is None:
            raise serializers.ValidationError("paymentPackage doesn't exist")
        elif paymentPackage.fare is not None:
            if json.get("hours") is None:
                raise serializers.ValidationError("hours field not provided")
        elif paymentPackage.custom is not None:
            if json.get("price") is None:
                raise serializers.ValidationError("price field not provided")
        if json.get("eventLocation_id") is None:
            raise serializers.ValidationError("eventLocation_id field not provided")
        eventLocation = EventLocation.objects.filter(pk=request.data.get("eventLocation_id")).first()
        if eventLocation is None:
            raise serializers.ValidationError("eventLocation doesn't exist")
        elif eventLocation.customer != customer:
            raise serializers.ValidationError("can't reference this eventLocation")
        return True




"""
class CreateOfferRequest(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ('description', 'date', 'hours', 'price', 'paymentPackage_id', 'eventLocation_id')

"""


