"""
Adds simple form view, which communicates with Braintree.
There are four steps to finally process a transaction:
1. Create a client token (views.py)
2. Send it to Braintree (js)
3. Receive a payment nonce from Braintree (js)
4. Send transaction details and payment nonce to Braintree (views.py)
"""
import braintree

from rest_framework import generics
from Server import settings
from rest_framework.response import Response
from .serializers import TransactionSerializer,PaypalSerializer2
from utils.authentication_utils import get_logged_user,get_user_type
from utils.Assertions import Assertions
from Grooving.models import Offer
from rest_framework import status
import requests
import braintree
import json
from requests.auth import HTTPBasicAuth
from utils.utils import check_accept_language
from .internationalization import translate


class BraintreeViews(generics.GenericAPIView):

    serializer_class = TransactionSerializer

    def get(self, request, format=None):

        language = check_accept_language(self.request)

        if settings.BRAINTREE_PRODUCTION:
            braintree_env = braintree.Environment.Production
        else:
            braintree_env = braintree.Environment.Sandbox

        Assertions.assert_true_raise400(braintree_env, translate(language, 'ERROR_ENVIROMENT'))

        # Configure Braintree
        braintree.Configuration.configure(
            environment=braintree_env,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY,
        )

        # Generate a client token. We'll send this to the form to
        # finally generate the payment nonce
        # You're able to add something like ``{"customer_id": 'foo'}``,
        # if you've already saved the ID
        self.braintree_client_token = braintree.ClientToken.generate({})

        Assertions.assert_true_raise400(self.braintree_client_token, translate(language, 'ERROR_TOKEN'))

        return Response(self.braintree_client_token)

    def post(self, request, *args, **kwargs):
        # Braintree customer info
        # You can, for sure, use several approaches to gather customer infos
        # For now, we'll simply use the given data of the user instance

        language = check_accept_language(self.request)

        logged_user = get_logged_user(request)
        type = get_user_type(logged_user)

        Assertions.assert_true_raise401(logged_user, translate(language, "ERROR_NOT_LOGGED_IN"))
        Assertions.assert_true_raise401(type == "Customer", translate(language, 'ERROR_NO_CUSTOMER'))

        if settings.BRAINTREE_PRODUCTION:
            braintree_env = braintree.Environment.Production
        else:
            braintree_env = braintree.Environment.Sandbox

        Assertions.assert_true_raise400(braintree_env, translate(language, 'ERROR_ENVIROMENT'))
        # Configure Braintree

        gateway = braintree.BraintreeGateway(
            braintree.Configuration(
                braintree.Environment.Sandbox,
                merchant_id=settings.BRAINTREE_MERCHANT_ID,
                public_key=settings.BRAINTREE_PUBLIC_KEY,
                private_key=settings.BRAINTREE_PRIVATE_KEY
            )
        )

        serializer = TransactionSerializer(data=request.data, partial=True)
        serializer.is_valid()

        """
        Create a new transaction and submit it.
        I don't gather the whole address in this example, but I can
        highly recommend to do that. It will help you to avoid any
        fraud issues, since some providers require matching addresses
        """

        # You can use the form to calculate a total or add a static total amount
        # I'll use a static amount in this example
        customer_kwargs = {
            "first_name": logged_user.user.first_name,
            "last_name": logged_user.user.last_name,
            "email": logged_user.user.email,
        }

        #if request.data['paypalCustomer'] is None or request.data['paypalCustomer'] == "":

        customer = gateway.customer.create(customer_kwargs)
        Assertions.assert_true_raise400(serializer.data['payment_method_nonce'], translate(language, 'ERROR_INCORRECT_ID'))
        Assertions.assert_true_raise400(customer, translate(language, 'ERROR_CUSTOMER'))
        Assertions.assert_true_raise400(serializer.data['id_offer'], translate(language, "ERROR_NO_OFFER"))

        offer = Offer.objects.filter(id=serializer.data['id_offer']).first()
        Assertions.assert_true_raise400(offer, translate(language, "ERROR_NO_OFFER"))

        Assertions.assert_true_raise401(offer.eventLocation.customer.user_id == logged_user.user_id, translate(language, 'ERROR_OFFER_CUSTOMER'))

        if offer.paymentPackage.performance is not None:
            amount = offer.paymentPackage.performance.price
        else:
            amount = offer.price * offer.hours

        Assertions.assert_true_raise400(amount > 0, translate(language, 'ERROR_AMOUNT'))

        result = gateway.transaction.sale({
            "customer_id": customer.customer.id,
            "amount": str(amount),
            "payment_method_nonce": serializer.data['payment_method_nonce'],
            "options": {
                # Use this option to store the customer data, if successful
                'store_in_vault_on_success': True,
                # Use this option to directly settle the transaction
                # If you want to settle the transaction later, use ``False`` and later on
                # ``braintree.Transaction.submit_for_settlement("the_transaction_id")``
                'submit_for_settlement': False
            }
        })

        if not result.is_success:

            for error in result.errors.deep_errors:
                print(error.attribute)
                print(error.code)
                print(error.message)

            for error in result.errors.for_object("customer"):
                print(error.attribute)
                print(error.code)
                print(error.message)

            for error in result.errors.for_object("customer").for_object("credit_card"):
                print(error.attribute)
                print(error.code)
                print(error.message)
            # Card could've been declined or whatever
            # I recommend to send an error report to all admins
            # , including ``result.message`` and ``self.user.email``
            context = {
                'error': "Failed to validate",
                'form': request.data,
                'braintree_error': (
                    'Your payment could not be processed. Please check your'
                    ' input or use another payment method and try again.')
            }
            if not result.is_success:
                offer.delete()
            Assertions.assert_true_raise400(result.is_success, translate(language, 'ERROR_PAYMENT'))



        offer.transaction.braintree_id = result.transaction.id
        offer.transaction.amount = amount
        offer.transaction.save()
        offer.save()

        # Finally there's the transaction ID
        # You definitely want to send it to your database
        # Now you can send out confirmation emails or update your metrics
        # or do whatever makes you and your customers happy :)
        return Response()


class PayPaypal(generics.GenericAPIView):

    serializer_class = PaypalSerializer2

    def post(self, request, *args, **kwargs):

        language = check_accept_language(self.request)

        logged_user = get_logged_user(request)
        type = get_user_type(logged_user)

        Assertions.assert_true_raise401(logged_user, translate(language, "ERROR_NOT_LOGGED_IN"))
        Assertions.assert_true_raise401(type == "Customer", translate(language, 'ERROR_NO_CUSTOMER'))

        serializer = PaypalSerializer2(data=request.data, partial=True)
        serializer.is_valid()

        Assertions.assert_true_raise400(serializer.data['authorization_id'], translate(language, 'ERROR_INCORRECT_ID'))

        Assertions.assert_true_raise400(serializer.data['id_offer'], translate(language, "ERROR_NO_OFFER"))
        offer = Offer.objects.filter(id=serializer.data['id_offer']).first()
        Assertions.assert_true_raise400(offer, translate(language, "ERROR_NO_OFFER"))

        Assertions.assert_true_raise401(offer.eventLocation.customer.user_id == logged_user.user_id,
                                        translate(language, 'ERROR_OFFER_CUSTOMER'))

        if offer.paymentPackage.performance is not None:
            amount = offer.paymentPackage.performance.price
        else:
            amount = offer.price * offer.hours

        Assertions.assert_true_raise400(amount > 0, translate(language, 'ERROR_AMOUNT'))

        response = requests.post('https://api.sandbox.paypal.com/v1/oauth2/token',
                                 headers={'Accept': 'application/json', 'Accept-Language': 'en_US',
                                          'content-type': 'application/x-www-form-urlencoded'},
                                 params={'grant_type': 'client_credentials'},
                                 auth=HTTPBasicAuth(
                                     'AVwB_2wUfHN5UCJO1Ik6uWkFbALgetwYKS5_BJ6gr9bR6wcEP5iFK84Nme_ebMbXI4yQdgH5BX2Tld2o',
                                     'EEZqYac8yorxpDQNojGYT0vWxP6VVBDIOSCuCgyQB6B7zTwdEG1uuRZS52DytG-qlLAY1vtMrZG60hgB'))

        Assertions.assert_true_raise400(response, translate(language, 'ERROR_CREDENTIAL'))

        access_token = json.loads(response.content.decode("utf-8"))['access_token']

        response2 = requests.post('https://api.sandbox.paypal.com/v2/checkout/orders/'+serializer.data['authorization_id']+'/authorize',
                                  headers={'content-type': 'application/json',
                                           'authorization': 'Bearer ' + access_token})

        Assertions.assert_true_raise400(response2, translate(language, 'ERROR_RESPONSE'))

        print(response2.json())
        offer.transaction.braintree_id = response2.json()['purchase_units'][0]['payments']['authorizations'][0]['id']
        offer.transaction.amount = amount
        offer.transaction.save()
        offer.save()

        return Response(response2.json(), status=status.HTTP_201_CREATED)
