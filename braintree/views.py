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


class CheckoutView(generics.RetrieveUpdateDestroyAPIView):

    def post(self, request, *args, **kwargs):
        # We need the user to assign the transaction
        self.user = request.user

        # Ha! There it is. This allows you to switch the
        # Braintree environments by changing one setting
        if settings.BRAINTREE_PRODUCTION:
            braintree_env = braintree.Environment.Production
        else:
            braintree_env = braintree.Environment.Sandbox

        # Configure Braintree
        braintree.Configuration.configure(
            braintree_env,
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



class InfoView(generics.RetrieveUpdateDestroyAPIView):

    def post(self, request, *args, **kwargs):
        # Braintree customer info
        # You can, for sure, use several approaches to gather customer infos
        # For now, we'll simply use the given data of the user instance
        customer_kwargs = {
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
        }

        # Create a new Braintree customer
        # In this example we always create new Braintree users
        # You can store and re-use Braintree's customer IDs, if you want to
        result = braintree.Customer.create(customer_kwargs)
        if not result.is_success:
            # Ouch, something went wrong here
            # I recommend to send an error report to all admins
            # , including ``result.message`` and ``self.user.email``

            context = self.get_context_data()
            # We re-generate the form and display the relevant braintree error
            context.update({
                'body': request.data,
                'braintree_error': u'{} {}'.format(
                    result.message, _('Please get in contact.'))
            })
            return self.render_to_response(context)

        # If the customer creation was successful you might want to also
        # add the customer id to your user profile
        customer_id = result.customer.id

        """
        Create a new transaction and submit it.
        I don't gather the whole address in this example, but I can
        highly recommend to do that. It will help you to avoid any
        fraud issues, since some providers require matching addresses

        """
        address_dict = {
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "street_address": 'street',
            "extended_address": 'street_2',
            "locality": 'city',
            "region": 'state_or_region',
            "postal_code": 'postal_code',
            "country_code_alpha2": 'alpha2_country_code',
            "country_code_alpha3": 'alpha3_country_code',
            "country_name": 'country',
            "country_code_numeric": 'numeric_country_code',
        }

        # You can use the form to calculate a total or add a static total amount
        # I'll use a static amount in this example

        result = braintree.Transaction.sale({
            "customer_id": customer_id,
            "amount": 100,
            "payment_method_nonce": request.get('payment_method_nonce'),
            "descriptor": {
                # Definitely check out https://developers.braintreepayments.com/reference/general/validation-errors/all/python#descriptor
                "name": "COMPANY.*test",
            },
            "billing": address_dict,
            "shipping": address_dict,
            "options": {
                # Use this option to store the customer data, if successful
                'store_in_vault_on_success': True,
                # Use this option to directly settle the transaction
                # If you want to settle the transaction later, use ``False`` and later on
                # ``braintree.Transaction.submit_for_settlement("the_transaction_id")``
                'submit_for_settlement': False,
            },
        })
        if not result.is_success:
            # Card could've been declined or whatever
            # I recommend to send an error report to all admins
            # , including ``result.message`` and ``self.user.email``
            context = self.get_context_data()
            context.update({
                'form': request.data,
                'braintree_error': _(
                    'Your payment could not be processed. Please check your'
                    ' input or use another payment method and try again.')
            })
            return Response()

        # Finally there's the transaction ID
        # You definitely want to send it to your database
        transaction = Transaction.objects.get()
        transaction_id = result.transaction.id
        transaction.id = transaction_id
        # Now you can send out confirmation emails or update your metrics
        # or do whatever makes you and your customers happy :)
        return Response()

    def get_context_data(self, **kwargs):
        ctx = super(CheckoutView, self).get_context_data(**kwargs)
        ctx.update({
            'braintree_client_token': self.braintree_client_token,
        })
        return ctx