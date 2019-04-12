from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import FieldError
from Grooving.models import Offer, PaymentPackage, EventLocation, Customer, Artist, Transaction, Rating, \
    SystemConfiguration
from utils.Assertions import assert_true, Assertions
from django.db import IntegrityError
from decimal import Decimal
import random
import string
import datetime
import pycard
from validate_email_address import validate_email
from django.utils import timezone
from utils.authentication_utils import get_user_type
from utils.notifications.notifications import Notifications
from Server import settings
import requests
import braintree
import json
from requests.auth import HTTPBasicAuth


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

    amount = serializers.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'paypalArtist')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('score', 'comment')


class GetOfferSerializer(serializers.ModelSerializer):

    paymentPackage = PaymentPackageSerializer(read_only=True)
    paymentPackage_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PaymentPackage.objects.all(),
                                                           source='paymentPackage')
    eventLocation = EventLocationSerializer(read_only=True)
    eventLocation_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=EventLocation.objects.all(),
                                                          source='eventLocation')

    rating = RatingSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = ('id', 'reason', 'appliedVAT', 'description', 'status', 'date', 'hours', 'price', 'currency',
                  'paymentPackage', 'paymentPackage_id', 'eventLocation', 'eventLocation_id', 'rating')


class OfferSerializer(serializers.ModelSerializer):

    paymentPackage = PaymentPackageSerializer(read_only=True)
    paymentPackage_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=PaymentPackage.objects.all(),
                                                               source='paymentPackage')
    eventLocation = EventLocationSerializer(read_only=True)
    eventLocation_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=EventLocation.objects.all(),
                                                              source='eventLocation')
    # transaction = TransactionSerializer()

    rating = RatingSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = ('id', 'reason', 'appliedVAT', 'description', 'status', 'date', 'hours', 'price', 'currency',
                      'paymentPackage', 'paymentPackage_id', 'eventLocation', 'eventLocation_id','rating')

    # Esto sobrescribe una función heredada del serializer.
    def save(self, pk=None, logged_user=None):
        if self.initial_data.get('id') is None and pk is None:
            # creation
            offer = Offer()
            offer = self._service_create(self.initial_data, offer, logged_user)
            Notifications.send_email_create_an_offer(offer.id) # TODO
        else:
            # edit
            id = (self.initial_data, pk)[pk is not None]

            offer = Offer.objects.filter(pk=id).first()
            offer = self._service_update(self.initial_data, offer, logged_user)

        return offer

    @staticmethod
    def service_made_payment_artist(paymentCode, user_logged):
        Assertions.assert_true_raise403(user_logged is not None)
        Assertions.assert_true_raise400(paymentCode is not None, {"error": "null payment code"})

        offer = Offer.objects.filter(paymentCode=paymentCode).first()
        Assertions.assert_true_raise404(offer, {'error': 'Offer not found'})
        Assertions.assert_true_raise403(offer.paymentPackage.portfolio.artist.id == user_logged.id,
                                            {'error': 'You are not the owner of the offer'})
        Assertions.assert_true_raise400(offer.status == 'CONTRACT_MADE',
                                        {"error": 'The payment has already been made or is outdated'})

        offer.status = 'PAYMENT_MADE'

        # Configure Paypal
        response = requests.post('https://api.sandbox.paypal.com/v1/oauth2/token',
                      headers={'Accept': 'application/json', 'Accept-Language': 'en_US', 'content-type': 'application/x-www-form-urlencoded'},
                      params={'grant_type': 'client_credentials'},
                      auth=HTTPBasicAuth('AZUNfuWGR6SWVjXJo82ariPtUrGOgA7L_QP2sxe8_QHaBuQ2JUT7AN9KnQKTpjT20yOr8l4G_3zlvx3B',
                                         'EPyiDZA9P9vGWLXihX-p5qTfVBZRtMvE1gCV5G2eLHgzbZXWo5VlctjQgIIUr1WPZT-haW5Db_pDJ-3t'))

        Assertions.assert_true_raise400(response, {'error': 'No hay respuesta desde Paypal'})

        access_token = json.loads(response.content.decode("utf-8"))['access_token']

        Assertions.assert_true_raise400(response, {'error': 'No coge el token'})
        Assertions.assert_true_raise401(user_logged.paypalAccount,
                                        {'paypal': ' You need to provide a PayPal account to perform this action' })

        response = requests.post('https://api.sandbox.paypal.com/v1/payments/payouts',
                                 data='{"sender_batch_header": {"sender_batch_id": "Payment_Offer_'+str(paymentCode)+'","email_subject": "You have a payout!","email_message": "You have received a payout! Thanks for using our service!"},"items": [{"recipient_type": "EMAIL","amount": {"value": "'+str(offer.transaction.amount)+'","currency": "EUR"},"note": "Thanks for your patronage!","receiver": "'+str(user_logged.paypalAccount)+'"}]}',
                                 headers={'content-type': 'application/json',
                                          'authorization': 'Bearer ' + access_token})

        Assertions.assert_true_raise400(response, {'error': 'No hay respuesta AL PAGAR'})
        # except:
        # offer.status == 'CONTRACT_MADE'
        offer.save()

        # Notification by email
        Notifications.send_email_contract_made_to_payment_made(offer.id)

        return offer

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
        #Assertions.assert_true_raise400(json.get('transaction').get('amount'), {'error' : 'No amount recieved'})
        #transaction.amount = json.get('transaction').get('amount')

        transaction.save()

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
        Assertions.assert_true_raise400(json_status, {'error': 'status field not provided'})
        if json_status:
            status_in_db = offer_in_db.status
            Assertions.assert_true_raise400(json_status != status_in_db, {'error': 'status provided isn\'t changed'})
            normal_transitions = {}
            artist_flowstop_transitions = {}
            customer_flowstop_transitions = {}

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
                    print(logged_user.paypalAccount)
                    Assertions.assert_true_raise400(logged_user.paypalAccount,
                                        {'error': ' You need to provide a PayPal account to perform this action' })
                    transaccion = offer_in_db.transaction

                    transaccion.paypalArtist = logged_user.paypalAccount

                    transaccion.save()

                    if settings.BRAINTREE_PRODUCTION:
                        braintree_env = braintree.Environment.Production
                    else:
                        braintree_env = braintree.Environment.Sandbox

                    Assertions.assert_true_raise400(braintree_env, {'error': 'Enviroment in Braintree not set'})

                    # Configure Braintree
                    braintree.Configuration.configure(
                        environment=braintree_env,
                        merchant_id=settings.BRAINTREE_MERCHANT_ID,
                        public_key=settings.BRAINTREE_PUBLIC_KEY,
                        private_key=settings.BRAINTREE_PRIVATE_KEY,
                    )
                    Assertions.assert_true_raise400(offer_in_db.transaction.braintree_id,{'error':
                    'La oferta no posee los credenciales de Braintree'})
                    braintree.Transaction.submit_for_settlement(offer_in_db.transaction.braintree_id)
                elif json_status == 'REJECTED':

                    if settings.BRAINTREE_PRODUCTION:
                        braintree_env = braintree.Environment.Production
                    else:
                        braintree_env = braintree.Environment.Sandbox

                    Assertions.assert_true_raise400(braintree_env, {'error': 'Enviroment in Braintree not set'})

                    # Configure Braintree
                    braintree.Configuration.configure(
                        environment=braintree_env,
                        merchant_id=settings.BRAINTREE_MERCHANT_ID,
                        public_key=settings.BRAINTREE_PUBLIC_KEY,
                        private_key=settings.BRAINTREE_PRIVATE_KEY,
                    )

                    #braintree.Transaction.settlement_decline_transaction(offer_in_db.transaction.braintree_id)

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

            # Sending email notifications

            if offer_in_db.status == 'CONTRACT_MADE':
                Notifications.send_email_pending_to_contract_made(offer_in_db.id)
            elif offer_in_db.status == 'REJECTED':
                Notifications.send_email_pending_to_rejected(offer_in_db.id)
            elif offer_in_db.status == 'WITHDRAWN':
                Notifications.send_email_pending_to_withdrawn(offer_in_db.id)
            elif offer_in_db.status == 'CANCELLED_ARTIST':
                Notifications.send_email_contract_made_to_cancelled_artist(offer_in_db.id)
            elif offer_in_db.status == 'CANCELLED_CUSTOMER':
                Notifications.send_email_contract_made_to_cancelled_customer(offer_in_db.id)

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

        Assertions.assert_true_raise400(json.get("description"),
                                        {'error': 'description field not provided'})
        Assertions.assert_true_raise400(json.get("date"),
                                        {'error': 'date field not provided'})

        # Past date value validation

        try:    
            datetime.datetime.strptime(json.get('date'), '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            Assertions.assert_true_raise400(False, {'error': 'The format is not correct. It should be YYYY-MM-DDTHH:mm:ss'})

        Assertions.assert_true_raise400(datetime.datetime.strptime(json.get('date'),
                                                                   '%Y-%m-%dT%H:%M:%S') > datetime.datetime.now(),
                                        {'error': 'date value is past'})
        Assertions.assert_true_raise400(json.get("paymentPackage_id"),
                                        {'error': 'payment package field not provided'})

        paymentPackage = PaymentPackage.objects.filter(pk=json.get("paymentPackage_id")).first()

        Assertions.assert_true_raise400(paymentPackage,
                                        {'error': 'payment package doesn\'t exist'})

        # Custom offer properties for each paymentPackage type

        if paymentPackage.fare is not None:
            Assertions.assert_true_raise400(json.get("hours"),
                                            {'error': 'hours field not provided'})
            try:
                decimal = json.get("hours")-int(json.get("hours"))
                Assertions.assert_true_raise400(decimal == 0.5 or decimal == 0.0,
                                                {'error': 'hours value bad provided'})
            except Exception:
                raise Assertions.assert_true_raise400(False, {'error': 'hours value bad provided'})

        elif paymentPackage.custom is not None:
            Assertions.assert_true_raise400(json.get("price"),
                                            {'error': 'price field not provided'})
            Assertions.assert_true_raise400(Decimal(0.0 < json.get("price")) >= paymentPackage.custom.minimumPrice,
                                            {'error': 'price entered it\'s below of minimum price'})
            Assertions.assert_true_raise400(json.get('hours'),
                                            {'error': 'hours field not provided'})

        Assertions.assert_true_raise400(json.get("eventLocation_id"),
                                        {'error': 'event location field not provided'})

        eventLocation = EventLocation.objects.filter(pk=attrs.data.get("eventLocation_id")).first()

        Assertions.assert_true_raise400(eventLocation,
                                        {'error': 'event location does not exist'})

        # User owner validation

        Assertions.assert_true_raise400(eventLocation.customer.user.id == attrs.user.id,
                                        {'error': 'can\'t reference this eventLocation'})

        return True

