from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from Grooving.models import Offer, PaymentPackage, EventLocation, Customer, Artist, Transaction, Rating, \
    SystemConfiguration
from utils.Assertions import assert_true, Assertions
from django.db import IntegrityError
from decimal import Decimal
import random
import string
import datetime
from django.utils import timezone
from utils.authentication_utils import get_logged_user, get_user_type


class PaymentPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentPackage
        fields = ('id', 'description', 'portfolio_id', 'performance_id', 'fare_id', 'custom_id')


class EventLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLocation
        fields = ('id', 'address', 'equipment', 'description')


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('paymentCode',)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('holder', 'expirationDate', 'number', 'cvv', 'ibanCustomer', 'paypalCustomer', 'ibanArtist',
                  'paypalArtist')

    def validate(self, attrs):
        # if attrs.get('ibanCustomer') is not None:
        if attrs.get('paypalCustomer') is None:
            Assertions.assert_true_raise400(
                # attrs.get('ibanCustomer') is not None and
                attrs.get('holder') is not None and
                attrs.get('number') is not None and
                attrs.get('expirationDate') is not None and
                attrs.get('cvv') is not None,
                {'error': 'credit card value doesn\'t valid'}
            )
        else:
            Assertions.assert_true_raise400(attrs.get('paypalCustomer'),
                                            {'error': 'paypal customer value doesn\'t valid'})
        return True


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('score', 'comment')


class OfferSerializer(serializers.ModelSerializer):
    paymentPackage = PaymentPackageSerializer(read_only=True)
    paymentPackage_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PaymentPackage.objects.all(),
                                                           source='paymentPackage')
    eventLocation = EventLocationSerializer(read_only=True)
    eventLocation_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=EventLocation.objects.all(),
                                                          source='eventLocation')
    transaction = TransactionSerializer(partial=True)

    rating = RatingSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = ('id', 'reason', 'appliedVAT', 'description', 'status', 'date', 'hours', 'price', 'currency',
                  'paymentCode', 'paymentPackage', 'paymentPackage_id', 'eventLocation', 'eventLocation_id',
                  'transaction', 'rating')

    # Esto sobrescribe una función heredada del serializer.
    def save(self, pk=None, logged_user=None):
        if self.initial_data.get('id') is None and pk is None:
            # creation
            offer = Offer()
            offer = self._service_create(self.initial_data, offer, logged_user)
        else:
            # edit
            id = (self.initial_data, pk)[pk is not None]

            offer = Offer.objects.filter(pk=id).first()
            offer = self._service_update(self.initial_data, offer, logged_user)

        return offer

    @staticmethod
    def service_made_payment_artist(paymentCode, user_logged):
        Assertions.assert_true_raise403(user_logged is not None)
        Assertions.assert_true_raise400(paymentCode is not None, {"paymentCode": "null payment code"})

        offer = Offer.objects.filter(paymentCode=paymentCode).first()
        Assertions.assert_true_raise404(offer is not None)
        Assertions.assert_true_raise403(offer.paymentPackage.portfolio.artist.id == user_logged.id)
        Assertions.assert_true_raise400(offer.status == 'CONTRACT_MADE',
                                        {"status": 'El pago ya se ha hecho o no se puede realizar ya'})

        offer.status = 'PAYMENT_MADE'
        # try:
        # TODO: Pago por braintree
        # except:
        # offer.status == 'CONTRACT_MADE'
        offer.save()

    # Se pondrá service delante de nuestros métodos para no sobrescribir por error métodos del serializer
    @staticmethod
    def _service_create(json: dict, offer: Offer, logged_user: User):
        offer.description = json.get('description')
        offer.date = datetime.datetime.strptime(json.get('date'), "%Y-%m-%dT%H:%M:%S")
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

        transaction = Transaction()
        if json.get('transaction').get('paypalCustomer') is not None:
            transaction = Transaction.objects.create(
                paypalCustomer=json.get('transaction').get('paypalCustomer'),
            )
            Customer.objects.filter(user_id=logged_user.id).update(
                paypalAccount=transaction.paypalCustomer,
            )
        else:
            transaction = Transaction.objects.create(
                # ibanCustomer=json.get('transaction').get('ibanCustomer'),
                holder=json.get('transaction').get('holder'),
                number=json.get('transaction').get('number'),
                expirationDate=datetime.datetime.strptime(json.get('transaction').get('expirationDate'), "%m%y").date(),
                cvv=json.get('transaction').get('cvv')
            )
            Customer.objects.filter(user_id=logged_user.id).update(
                # ibanCustomer=json.get('transaction').get('ibanCustomer'),
                holder=transaction.holder,
                number=transaction.number,
                expirationDate=transaction.expirationDate
            )
        offer.transaction = transaction
        offer.appliedVAT = SystemConfiguration.objects.all().first().vat
        offer.save()
        return offer

    def _service_update(self, json: dict, offer_in_db: Offer, logged_user: User):
        assert_true(offer_in_db, "This offer does not exist")
        print(offer_in_db.date)
        now = timezone.now()

        assert_true(offer_in_db.date > now, "The offer ocurred in the past")
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
                                                 'CONTRACT_MADE': 'CANCELLED_CUSTOMER'}

            artistReceiver = Artist.objects.filter(pk=offer_in_db.paymentPackage.portfolio.artist.id).first()

            if get_user_type(logged_user) == 'Artist' and artistReceiver == logged_user:
                normal_transitions = {'PENDING': 'CONTRACT_MADE'}
                artist_flowstop_transitions = {'PENDING': 'REJECTED',
                                               'CONTRACT_MADE': 'CANCELLED_ARTIST'}
                if json_status == 'CONTRACT_MADE':
                    Assertions.assert_true_raise400(logged_user.iban is not None,
                                                    {"ERROR_CODE:""You must introduce your bank account before"})

            allowed_transition = (normal_transitions.get(status_in_db) == json_status
                                  or artist_flowstop_transitions.get(status_in_db) == json_status
                                  or customer_flowstop_transitions.get(status_in_db) == json_status
                                  or status_in_db == json_status
                                  )

            assert_true(allowed_transition, "Not allowed status transition: " + status_in_db + " to "
                        + json_status + ".")

            if json_status == "CONTRACT_MADE":
                while True:

                    try:
                        offer_in_db.paymentCode = self._service_generate_unique_payment_code()
                        offer_in_db.save()
                        break
                    except IntegrityError:
                        continue

            print("ESTADO DB ANTES:" + offer_in_db.status)
            offer_in_db.status = json_status
            offer_in_db.reason = json.get('reason')
            if json_status == "CONTRACT_MADE" or json_status == "PAYMENT_MADE":
                offer_in_db.reason = None
            offer_in_db.save()
            print("ESTADO DB DESPUES:" + offer_in_db.status)
            return offer_in_db

    @staticmethod
    def _service_generate_unique_payment_code():
        random_alphanumeric = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        payment_code = random_alphanumeric
        return payment_code

    def validate(self, attrs):

        # Customer validation

        customer = Customer.objects.filter(user_id=attrs.user.id).first()

        Assertions.assert_true_raise403(customer is not None, {'error': 'user isn\'t authorized'})

        # Body request validation

        json = attrs.data

        Assertions.assert_true_raise400(json.get("description") is not None,
                                        {'error': 'description field not provided'})
        Assertions.assert_true_raise400(json.get("date") is not None,
                                        {'error': 'date field not provided'})
        Assertions.assert_true_raise400(json.get("transaction") is not None,
                                        {'error': 'transaction field not provided'})

        TransactionSerializer.validate(self, json.get("transaction"))

        # Past date value validation

        Assertions.assert_true_raise400(datetime.datetime.strptime(json.get('date'),
                                                                   '%Y-%m-%dT%H:%M:%S') > datetime.datetime.now(),
                                        {'error': 'date value is past'})
        Assertions.assert_true_raise400(json.get("paymentPackage_id") is not None,
                                        {'error': 'paymentPackage_id field not provided'})

        paymentPackage = PaymentPackage.objects.filter(pk=json.get("paymentPackage_id")).first()

        Assertions.assert_true_raise400(paymentPackage is not None,
                                        {'error': 'paymentPackage doesn\'t exist'})

        # Custom offer properties for each paymentPackage type

        if paymentPackage.fare is not None:
            Assertions.assert_true_raise400(json.get("hours") is not None,
                                            {'error': 'hours field not provided'})
        elif paymentPackage.custom is not None:
            Assertions.assert_true_raise400(json.get("price") is not None,
                                            {'error': 'price field not provided'})
            Assertions.assert_true_raise400(Decimal(json.get("price")) > paymentPackage.custom.minimumPrice,
                                            {'error': 'price entered it\'s below of minimum price'})
            Assertions.assert_true_raise400(json.get("hours") is not None,
                                            {'error': 'hours field not provided'})

        Assertions.assert_true_raise400(json.get("eventLocation_id") is not None,
                                        {'error': 'eventLocation_id field not provided'})

        eventLocation = EventLocation.objects.filter(pk=attrs.data.get("eventLocation_id")).first()

        Assertions.assert_true_raise400(eventLocation is not None,
                                        {'error': 'eventLocation doesn\'t exist'})

        # User owner validation

        Assertions.assert_true_raise400(eventLocation.customer.user.id == attrs.user.id,
                                        {'error': 'can\'t reference this eventLocation'})

        return True


"""
class CreateOfferRequest(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ('description', 'date', 'hours', 'price', 'paymentPackage_id', 'eventLocation_id')

"""
