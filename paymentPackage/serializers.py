from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import PaymentPackage, Custom, Fare, Performance
from decimal import Decimal
from utils.Assertions import assert_true


class CurrencySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PaymentPackage
        fields = ('currency',)


class CustomSerializer(serializers.HyperlinkedModelSerializer):

    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = Custom
        fields = ('id', 'minimumPrice', 'currency')


class FareSerializer(serializers.HyperlinkedModelSerializer):

    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = Fare
        fields = ('id', 'priceHour', 'currency')


class PerformanceSerializer(serializers.HyperlinkedModelSerializer):

    currency = CurrencySerializer(read_only=True)

    class Meta:
        model = Performance
        fields = ('id', 'info', 'hours', 'price', 'currency')


class PaymentPackageSerializer(serializers.ModelSerializer):
    custom = CustomSerializer(read_only=True)
    fare = FareSerializer(read_only=True)
    performance = PerformanceSerializer(read_only=True)

    class Meta:
        model = PaymentPackage
        fields = ('id', 'description', 'custom', 'custom_id', 'fare', 'fare_id', 'performance', 'performance_id')

    @staticmethod
    def list_payment(self):

        paymentPackage = PaymentPackage.objects.get(pk=self.id)
        package = ""
        if paymentPackage.performance is not None:
            package = package + "{type: Performance,"
        elif paymentPackage.custom is not None:
            package = "Custom"
        elif paymentPackage.fare is not None:
            package = "Fare"
        return package

    def save(self):
        if self.initial_data.get('id') is None:
            # creation
            paymentPackage = PaymentPackage()
            paymentPackage = self._service_create(self.initial_data, paymentPackage)
        else:
            # edit
            print("Clave primaria:" + str(self.initial_data.get('id')))
            paymentPackage = PaymentPackage.objects.get(pk=self.initial_data.get('id'))
            paymentPackage = self._service_update(self.initial_data, paymentPackage)
            print(paymentPackage)
        paymentPackage.save()
        return paymentPackage

    @staticmethod
    def _service_create(json: dict, paymentPackage: PaymentPackage):
        paymentPackage.description = json.get('description')
        paymentPackage.appliedVAT = json.get('appliedVAT')
        paymentPackage.portfolio_id = json.get('portfolio_id')

        if json['performance'] is not None:
            performance = Performance()
            performance.hours = Decimal(json['performance']['hours'])
            performance.price = Decimal(json['performance']['price'])
            performance.currency = json['performance']['currency']
            performance.save()
            paymentPackage.performance_id = performance.id
        elif json['fare'] is not None:
            fare = Fare()
            fare.priceHour = Decimal(json['fare']['priceHour'])
            fare.currency = json['fare']['currency']
            fare.save()
            paymentPackage.fare_id = fare.id
        elif json['custom'] is not None:
            custom = Custom()
            custom.price = Decimal(json['custom']['price'])
            custom.currency = json['custom']['currency']
            custom.save()
            paymentPackage.custom_id = custom.id

        return paymentPackage

    @staticmethod
    def _service_update(json: dict, paymentPackage_in_db):

        print(paymentPackage_in_db)
        assert_true(paymentPackage_in_db, "No existe un paquete con esa id")

        paymentPackage_in_db.description = json.get('description')
        paymentPackage_in_db.appliedVAT = Decimal(json.get('appliedVAT'))

        if json['performance'] is not None:
            performance = Performance.objects.get(pk=json['performance']['id'])
            performance.hours = Decimal(json['performance']['hours'])
            performance.price = Decimal(json['performance']['price'])
            performance.currency = json['performance']['currency']
            performance.save()
        elif json['fare'] is not None:
            fare = Fare.objects.get(pk=json['fare']['id'])
            fare.priceHour = Decimal(json['fare']['priceHour'])
            fare.currency = json['fare']['currency']
            fare.save()
        elif json['custom'] is not None:
            custom = Custom.objects.get(pk=json['custom']['id'])
            custom.price = Decimal(json['custom']['price'])
            custom.currency = json['custom']['currency']
            custom.save()

        return paymentPackage_in_db


class PaymentPackageSerializerShort(serializers.ModelSerializer):

    paymentPackage = serializers.SerializerMethodField('list_payment')

    class Meta:
        model = PaymentPackage
        fields = ('id', 'description', 'currency', 'paymentPackage')

    @staticmethod
    def list_payment(self):

        paymentPackage = PaymentPackage.objects.get(pk=self.id)
        package = {}
        if paymentPackage.performance is not None:
            package['type'] = "Performance"
            package['info'] = paymentPackage.performance.info
            package['hours'] = paymentPackage.performance.hours
            package['price'] = paymentPackage.performance.price
        elif paymentPackage.custom is not None:
            package['type'] = "Custom"
            package['priceHour'] = paymentPackage.performance.priceHour
        elif paymentPackage.fare is not None:
            package['type'] = "Fare"
            package['minimumPrice'] = paymentPackage.performance.minimumPrice

        return package
