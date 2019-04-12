from rest_framework import serializers
from Grooving.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    payment_method_nonce = serializers.CharField()
    id_offer = serializers.CharField()

    class Meta:
        model = Transaction
        fields = ('id_offer', 'payment_method_nonce')
