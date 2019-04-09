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
from Grooving.models import Transaction
from .serializers import TransactionSerializer
from utils.authentication_utils import get_logged_user

class BraintreeViews(generics.GenericAPIView):

    serializer_class = TransactionSerializer

    def get(self, request, format=None):

        # We need the user to assign the transaction

        # Ha! There it is. This allows you to switch theself.braintree_client_token
        # Braintree environments by changing one setting

        if settings.BRAINTREE_PRODUCTION:
            braintree_env = braintree.Environment.Production
        else:
            braintree_env = braintree.Environment.Sandbox

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

        return Response(self.braintree_client_token)

    def post(self, request, *args, **kwargs):
        # Braintree customer info
        # You can, for sure, use several approaches to gather customer infos
        # For now, we'll simply use the given data of the user instance

        logged_user = get_logged_user(request)

        if settings.BRAINTREE_PRODUCTION:
            braintree_env = braintree.Environment.Production
        else:
            braintree_env = braintree.Environment.Sandbox

        # Configure Braintree
        braintree.Configuration.configure(
            environment=braintree_env,
            merchant_id=settings.BRAINTREE_MERCHANT_ID,
            public_key=settings.BRAINTREE_PUBLIC_KEY,
            private_key=settings.BRAINTREE_PRIVATE_KEY,
        )

        serializer = TransactionSerializer(data=request.data, partial=True)
        serializer.is_valid()
        """
        Create a new transaction and submit it.
        I don't gather the whole address in this example, but I can
        highly recommend to do that. It will help you to avoid any
        fraud issues, since some providers require matching addresses
        """
        i = 0
        year = "20"
        month = ""
        for char in serializer.data['expirationDate']:
            if i < 2:
                month += char
            elif i > 2:
                year += char
            i = i + 1
        print(month)
        print(year)
        number = ""
        i = 0

        for char in serializer.data['number']:
            if i < 6:
                number += char
            elif i > 5 and i < (len(serializer.data['number']) - 4):
                number += "*"
            elif i > (len(serializer.data['number']) - 5):
                number += char

            i = i + 1


        # You can use the form to calculate a total or add a static total amount
        # I'll use a static amount in this example
        customer_kwargs = {
            "first_name": logged_user.user.first_name,
            "last_name": logged_user.user.last_name,
            "email": logged_user.user.email,
        }

        customer = braintree.Customer.create(customer_kwargs)
        result = braintree.Transaction.sale({
            "customer_id": customer.customer.id,
            "amount": serializer.data['amount'],
            "credit_card": {
                "cardholder_name": serializer.data['holder'],
                "expiration_month": month,
                "expiration_year": year,
                "number": serializer.data['number'],
                "cvv": serializer.data['cvv']
            },
            "options":{
                # Use this option to store the customer data, if successful
                'store_in_vault_on_success': True,
                # Use this option to directly settle the transaction
                # If you want to settle the transaction later, use ``False`` and later on
                # ``braintree.Transaction.submit_for_settlement("the_transaction_id")``
                'submit_for_settlement': False,
            }
        })
        print(result.is_success)
        if not result.is_success:
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
            return Response(context)

        # Finally there's the transaction ID
        # You definitely want to send it to your database
        #transaction = Transaction.objects.get()
        #transaction_id = result.transaction.id
        #transaction.id = transaction_id
        # Now you can send out confirmation emails or update your metrics
        # or do whatever makes you and your customers happy :)
        return Response(serializer.data)
