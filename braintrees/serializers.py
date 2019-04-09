import braintree
from rest_framework import serializers
from Grooving.models import Transaction


class BraintreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('paypalCustomer',)
