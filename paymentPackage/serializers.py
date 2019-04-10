from django.contrib.auth.models import User, Group
from rest_framework import serializers
from Grooving.models import PaymentPackage, Custom, Fare, Performance,Portfolio
from decimal import Decimal
from utils.Assertions import assert_true
from django.core.exceptions import PermissionDenied
from utils.Assertions import Assertions
from utils.utils import isPositivefloat
from decimal import Decimal
class CurrencySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PaymentPackage
        fields = ('currency',)


class CustomPaymentPackageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Custom
        fields = ('minimumPrice',)


class FarePaymentPackageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Fare
        fields = ('priceHour',)


class PerformancePaymentPackageSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Performance
        fields = ('info', 'hours', 'price')

class PaymentPackageListSerializer(serializers.ModelSerializer):
    custom = CustomPaymentPackageSerializer(read_only=True)
    fare = FarePaymentPackageSerializer(read_only=True)
    performance = PerformancePaymentPackageSerializer(read_only=True)

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

class PaymentPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentPackage
        fields = ('description', 'custom', 'fare', 'performance')
'''
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
'''


class FareSerializer(serializers.ModelSerializer):

    paymentPackage = PaymentPackageSerializer()

    class Meta:
        model = Fare
        fields = ('priceHour', 'paymentPackage')

    def save(self, pk=None, logged_user=None):
        if pk is None:
            fare = self._service_create_package(self.initial_data,logged_user)
        else:
            fare= Fare.objects.filter(pk=pk).first()
            fare = self._service_update_package(self.initial_data, fare, logged_user)
        return fare

    @staticmethod
    def _service_create_package(json: dict, logged_user):

        priceHour = json.get('priceHour')
        description = json.get('description')

        Assertions.assert_true_raise400(priceHour, {'error': "Price not provided"})

        Assertions.assert_true_raise400(isPositivefloat(priceHour), {'error': "Invalid price"})

        portfolio = Portfolio.objects.filter(artist_id=logged_user.id).first()
        fare = Fare.objects.create(priceHour=json.get('priceHour'))
        PaymentPackage.objects.create(description=json.get('description'),
                                      portfolio_id=portfolio.id, fare=fare)

        return fare

    @staticmethod
    def _service_update_package(json: dict, fare: Fare, logged_user: User):
        assert_true(fare, "This offer does not exist")
        priceHour = json.get('priceHour')
        Assertions.assert_true_raise400(priceHour, {'error': "Price not provided"})
        Assertions.assert_true_raise400(isPositivefloat(priceHour), {'error': "Invalid price"})

        fare.priceHour=json.get('priceHour')
        fare.paymentpackage.description=json.get('description')
        fare.save()
        return fare

class CustomSerializer(serializers.ModelSerializer):

    paymentPackage = PaymentPackageSerializer()
    portfolio_id = serializers.CharField


    class Meta:
        model = Custom
        fields = ('minimumPrice', 'paymentPackage')

    def save(self, pk=None, logged_user=None):
        if pk is None:
            custom = self._service_create_package(self.initial_data, logged_user)
        else:
            custom = Custom.objects.filter(pk=pk).first()
            custom = self._service_update_package(self.initial_data, custom, logged_user)
        return custom

    @staticmethod
    def _service_create_package(json: dict, logged_user):

        minimumPrice = json.get('minimumPrice')
        description = json.get('description')

        Assertions.assert_true_raise400(minimumPrice, {'error': "Minimum price not provided"})

        Assertions.assert_true_raise400(isPositivefloat(minimumPrice), {'error': "Invalid price"})

        portfolio = Portfolio.objects.filter(artist_id=logged_user.id).first()
        custom = Custom.objects.create(minimumPrice=minimumPrice)
        PaymentPackage.objects.create(description=description,
                                      portfolio_id=portfolio.id, custom=custom)

        return custom

    @staticmethod
    def _service_update_package(json: dict, custom: Custom, logged_user: User):
        assert_true(custom, "This offer does not exist")
        minimumPrice = json.get('minimumPrice')
        Assertions.assert_true_raise400(minimumPrice, {'error': "Minimum price not provided"})

        Assertions.assert_true_raise400(isPositivefloat(minimumPrice), {'error': "Invalid price"})
        custom.minimumPrice = json.get('minimumPrice')
        custom.paymentpackage.description = json.get('description')
        custom.save()
        return custom


class PerformanceSerializer(serializers.ModelSerializer):

    paymentPackage = PaymentPackageSerializer()

    class Meta:
        model = Performance
        fields = ('info', 'hours', 'price', 'paymentPackage')

    def save(self, pk=None, logged_user=None):
        if pk is None:
            performance= self._service_create_package(self.initial_data, logged_user)
        else:
            performance = Performance.objects.filter(pk=pk).first()
            performance = self._service_update_package(self.initial_data, performance, logged_user)
        return performance

    @staticmethod
    def _service_create_package(json: dict, logged_user):
        hours = json.get('hours')
        description = json.get('description')
        info = json.get('info')
        price = json.get('price')
        Assertions.assert_true_raise400(hours, {'error': "Hours not provided"})
        Assertions.assert_true_raise400(info, {'error': "Info not provided"})
        Assertions.assert_true_raise400(price, {'error': "Price not provided"})

        Assertions.assert_true_raise400(isPositivefloat(hours), {'error': "Invalid hours"})
        Assertions.assert_true_raise400(isPositivefloat(price), {'error': "Invalid price"})

        portfolio = Portfolio.objects.filter(artist_id=logged_user.id).first()
        performance = Performance.objects.create(hours=json.get('hours'), info=json.get('info'), price=json.get('price'))
        PaymentPackage.objects.create(description=json.get('description'),
                                      portfolio_id=portfolio.id, performance=performance)

        return performance

    @staticmethod
    def _service_update_package(json: dict, performance: Performance, logged_user: User):
        assert_true(performance, "This offer does not exist")

        hours = json.get('hours')
        description = json.get('description')
        info = json.get('info')
        price = json.get('price')
        Assertions.assert_true_raise400(hours, {'error': "Hours not provided"})
        Assertions.assert_true_raise400(info, {'error': "Info not provided"})
        Assertions.assert_true_raise400(price, {'error': "Price not provided"})
        Assertions.assert_true_raise400(isPositivefloat(hours), {'error': "Invalid hours"})
        Assertions.assert_true_raise400(isPositivefloat(price), {'error': "Invalid price"})
        performance.hours = json.get('hours')
        performance.info = json.get('info')
        performance.price = json.get('price')
        performance.paymentpackage.description = json.get('description')
        performance.save()
        return performance


class PaymentPackageSerializerShort(serializers.ModelSerializer):

    paymentPackage = serializers.SerializerMethodField('list_payment')

    class Meta:
        model = PaymentPackage
        fields = ('id', 'description', 'paymentPackage')

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
