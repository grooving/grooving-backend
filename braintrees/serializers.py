from rest_framework import serializers
from Grooving.models import Transaction
from utils.Assertions import Assertions
import pycard
from validate_email_address import validate_email
from django.core.exceptions import FieldError


class TransactionSerializer(serializers.ModelSerializer):

    payment_method_nonce = serializers.CharField()
    amount = serializers.FloatField()
    expirationDate = serializers.DateField(input_formats='%m%y', format='%Y-%m')

    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'holder', 'expirationDate', 'number', 'cvv', 'paypalCustomer', 'payment_method_nonce')

    def validate(self, attrs):
        # if attrs.get('ibanCustomer') is not None:
        if attrs.get('paypalCustomer') is None:
            Assertions.assert_true_raise400(
                attrs.get('amount') and
                attrs.get('holder') and
                attrs.get('number') and
                attrs.get('expirationDate') and
                attrs.get('cvv'),
                {'error': 'credit card value doesn\'t valid'}
            )

            # Credit Card validation

            try:

                Assertions.assert_true_raise400(
                    len(attrs.get('amount')) > 0 and attrs.get('amount').isdigit() and int(attrs.get('amount')) > 0,
                    {'error': 'Error with the amount introduced'}
                )

                Assertions.assert_true_raise400(
                    len(attrs.get('number')) == 16 and attrs.get('number').isdigit(),
                    {'error': 'credit card number field bad provided'}
                )

                Assertions.assert_true_raise400(
                    len(attrs.get('expirationDate')) == 4 and attrs.get('expirationDate').isdigit(),
                    {'error': 'expiration date field bad provided'}
                )

                Assertions.assert_true_raise400(
                    len(attrs.get('cvv')) == 3 and attrs.get('cvv').isdigit(),
                    {'error': 'cvv field bad provided'}
                )

                number = attrs['number']
                cvc = attrs['cvv']

                month = int(attrs['expirationDate'][:2])
                year = attrs['expirationDate'][2:]
                year = '20' + year
                year = int(year)
                Assertions.assert_true_raise400(month >= 1 and  month<=12,
                    {'error':  'bad month number'}
                )
                card = pycard.Card(number=number, month=month, year=year,
                                   cvc=cvc)
                Assertions.assert_true_raise400(card.is_valid, {'error': 'The credit card is not valid.'})

            except FieldError:

                raise FieldError('Invalid credit card.')


        else:

            # Email validation

            Assertions.assert_true_raise400(validate_email(attrs.get('paypalCustomer')),
                                            {'error': 'paypal account provided isn\'t valid'})

        return True


