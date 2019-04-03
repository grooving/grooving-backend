from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from Grooving.models import Offer, PaymentPackage, EventLocation, Customer, Artist
from utils.Assertions import assert_true
from django.db import IntegrityError
from decimal import Decimal
import random
import string
import datetime
from django.utils import timezone
from utils.authentication_utils import get_logged_user,get_user_type,is_user_authenticated


class PaymentPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPackage
        fields = ('id', 'description', 'appliedVAT', 'portfolio_id', 'performance_id', 'fare_id', 'custom_id')


class EventLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLocation
        fields = ('id', 'address', 'equipment', 'description')


class OfferCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ('id', 'description', 'status', 'date', 'hours', 'price', 'paymentPackage',
                  'paymentPackage_id', 'eventLocation', 'eventLocation_id', 'paymentCode')


class OfferSerializer(serializers.ModelSerializer):

    paymentPackage = PaymentPackageSerializer(read_only=True)
    paymentPackage_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PaymentPackage.objects.all(),
                                                           source='paymentPackage')
    eventLocation = EventLocationSerializer(read_only=True)
    eventLocation_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=EventLocation.objects.all(),
                                                          source='eventLocation')

    class Meta:
        model = Offer
        fields = ('id', 'reason', 'appliedVAT', 'description', 'status', 'date', 'hours', 'price', 'currency',
                  'paymentCode', 'paymentPackage', 'paymentPackage_id', 'eventLocation', 'eventLocation_id',
                  'transaction', 'transaction_id', 'rating', 'rating_id')

    # Esto sobrescribe una función heredada del serializer.
    def save(self, pk=None, logged_user=None):
        if self.initial_data.get('id') is None and pk is None:
            # creation
            offer = Offer()
            offer = self._service_create(self.initial_data, offer)
        else:
            # edit
            id = (self.initial_data, pk)[pk is not None]

            offer = Offer.objects.filter(pk=id).first()
            offer = self._service_update(self.initial_data, offer, logged_user)

        return offer

    @staticmethod
    def service_made_payment_artist(paymentCode,user_logged):
        user_type = get_user_type(user_logged)
        if not None and user_type != "Artist":
            raise PermissionDenied("Only an artist can get the payment")

        offer = Offer.objects.filter(paymentCode=paymentCode).first()
        assert_true(offer, 'La oferta no existe')
        if offer.paymentPackage.portfolio.artist.id != user_logged.id:
            raise PermissionDenied("You are not the artist who was hired.")
        assert_true(offer.status == 'CONTRACT_MADE', 'Posiblemente el pago ya se ha hecho o no se puede realizar ya')
        
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
            offer.currency = offer.paymentPackage.currency
        elif offer.paymentPackage.fare is not None:
            offer.hours = json.get('hours')
            offer.price = offer.paymentPackage.fare.priceHour * Decimal(json.get('hours'))
            offer.currency = offer.paymentPackage.currency
        elif offer.paymentPackage.custom is not None:
            offer.hours = json.get('hours')
            offer.price = json.get('price')
            offer.currency = offer.paymentPackage.currency
        offer.save()
        return offer

    def _service_update(self, json: dict, offer_in_db: Offer, logged_user: User):
        assert_true(offer_in_db, "This offer does not exist")
        print(offer_in_db.date)
        now = timezone.now()

        assert_true(offer_in_db.date > now,"The offer ocurred in the past")
        offer = self._service_update_status(json, offer_in_db, logged_user)

        return offer

    def _service_update_status(self, json: dict, offer_in_db: Offer, logged_user: User):
        json_status = json.get('status')
        if json_status:
            status_in_db = offer_in_db.status
            normal_transitions = {}
            artist_flowstop_transitions = {}
            customer_flowstop_transitions = {}
            # TODO: Must be check the login

            creator = Customer.objects.filter(pk=offer_in_db.eventLocation.customer.id).first()
            if get_user_type(logged_user) == 'Customer' and creator == logged_user:
                customer_flowstop_transitions = {'PENDING': 'WITHDRAWN',
                                                 'CONTRACT_MADE': 'CANCELED'}

            artistReceiver = Artist.objects.filter(pk=offer_in_db.paymentPackage.portfolio.artist.id).first()
            print(artistReceiver)
            print(logged_user)
            if get_user_type(logged_user) == 'Artist' and artistReceiver == logged_user:
                normal_transitions = {'PENDING': 'CONTRACT_MADE'}
                artist_flowstop_transitions = {'PENDING': 'REJECTED',
                                               'CONTRACT_MADE': 'CANCELED'}


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

        # Customer validation

        customer = Customer.objects.filter(user_id=request.user.id).first()

        if customer is None:
            raise serializers.ValidationError("user isn't authorized")

        # Body request validation

        json = request.data

        if json.get("description") is None:
            raise serializers.ValidationError("description field not provided")
        if json.get("date") is None:
            raise serializers.ValidationError("date field not provided")

            # Past date value validation

        elif datetime.datetime.strptime(json.get('date'), '%Y-%m-%dT%H:%M:%S') < datetime.datetime.now():
            raise serializers.ValidationError("date value is past")

        if json.get("paymentPackage_id") is None:
            raise serializers.ValidationError("paymentPackage_id field not provided")
        else:
            paymentPackage = PaymentPackage.objects.filter(pk=json.get("paymentPackage_id")).first()

            if paymentPackage is None:
                raise serializers.ValidationError("paymentPackage doesn't exist")

            # Custom offer properties for each paymentPackage type

            elif paymentPackage.fare is not None:
                if json.get("hours") is None:
                    raise serializers.ValidationError("hours field not provided")

            elif paymentPackage.custom is not None:
                if json.get("price") is None:
                    raise serializers.ValidationError("price field not provided")
                elif Decimal(json.get("price")) < paymentPackage.custom.minimumPrice:
                    raise serializers.ValidationError("price entered it's below of minimum price")
                if json.get("hours") is None:
                    raise serializers.ValidationError("hours field not provided")

        if json.get("eventLocation_id") is None:
            raise serializers.ValidationError("eventLocation_id field not provided")
        eventLocation = EventLocation.objects.filter(pk=request.data.get("eventLocation_id")).first()
        if eventLocation is None:
            raise serializers.ValidationError("eventLocation doesn't exist")

        # User owner validation

        elif eventLocation.customer.user != request.user:
            raise serializers.ValidationError("can't reference this eventLocation")

        return True




"""
class CreateOfferRequest(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ('description', 'date', 'hours', 'price', 'paymentPackage_id', 'eventLocation_id')

"""


