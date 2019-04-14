from django.contrib.auth.models import User
from rest_framework import serializers
from Grooving.models import PaymentPackage, Custom, Fare, Performance
from utils.Assertions import assert_true
from utils.Assertions import Assertions
from utils.utils import isPositivefloat


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
        packages = PaymentPackage.objects.filter(portfolio_id=logged_user.portfolio.id)
        if packages:
            for package in packages:
                Assertions.assert_true_raise400(not package.fare_id, {'error': "You already have a fare package"})

        price_hour = json.get('priceHour')
        description = json.get('description')
        portfolio_id = logged_user.portfolio.id
        Assertions.assert_true_raise400(price_hour, {'error': "Price not provided"})

        Assertions.assert_true_raise400(isPositivefloat(price_hour), {'error': "Invalid price"})

        fare = Fare.objects.create(priceHour=price_hour)
        PaymentPackage.objects.create(description=description,
                                      portfolio_id=portfolio_id, fare=fare)

        return fare

    @staticmethod
    def _service_update_package(json: dict, fare: Fare, logged_user: User):
        assert_true(fare, "This offer does not exist")
        price_hour = json.get('priceHour')
        Assertions.assert_true_raise400(price_hour, {'error': "Price not provided"})
        Assertions.assert_true_raise400(isPositivefloat(price_hour), {'error': "Invalid price"})

        fare.priceHour = json.get('priceHour')
        fare.paymentpackage.description = json.get('description')
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

        packages = PaymentPackage.objects.filter(portfolio_id=logged_user.portfolio.id)
        if packages:
            for package in packages:
                Assertions.assert_true_raise400(not package.custom_id, {'error': "You already have a custom package"})

        minimum_price = json.get('minimumPrice')
        description = json.get('description')
        portfolio_id = logged_user.portfolio.id
        Assertions.assert_true_raise400(minimum_price, {'error': "Minimum price not provided"})

        Assertions.assert_true_raise400(isPositivefloat(minimum_price), {'error': "Invalid price"})

        custom = Custom.objects.create(minimumPrice=minimum_price)
        PaymentPackage.objects.create(description=description,
                                      portfolio_id=portfolio_id, custom=custom)

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
            performance = self._service_create_package(self.initial_data, logged_user)
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
        portfolio_id = logged_user.portfolio.id
        Assertions.assert_true_raise400(hours, {'error': "Hours not provided"})
        Assertions.assert_true_raise400(info, {'error': "Info not provided"})
        Assertions.assert_true_raise400(price, {'error': "Price not provided"})

        Assertions.assert_true_raise400(isPositivefloat(hours), {'error': "Invalid hours"})
        Assertions.assert_true_raise400(isPositivefloat(price), {'error': "Invalid price"})

        performance = Performance.objects.create(hours=json.get('hours'), info=json.get('info'), price=json.get('price'))
        PaymentPackage.objects.create(description=json.get('description'),
                                      portfolio_id=portfolio_id, performance=performance)

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
        performance.paymentpackage.description = description
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
