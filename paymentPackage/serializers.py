from rest_framework import serializers
from Grooving.models import PaymentPackage, Custom, Fare, Performance, SystemConfiguration
from utils.Assertions import Assertions
from utils.utils import isPositivefloat
from utils.utils import check_accept_language
from paymentPackage.internationalization import translate
from utils.utils import check_is_number


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

    def save(self, request, pk=None, logged_user=None):
        if pk is None:
            fare = self._service_create_package(self.initial_data, request, logged_user)
        else:
            fare = Fare.objects.filter(pk=pk).first()
            fare = self._service_update_package(self.initial_data, request, fare)
        return fare

    @staticmethod
    def _service_create_package(json: dict, request, logged_user):
        language = check_accept_language(request)
        packages = PaymentPackage.objects.filter(portfolio_id=logged_user.portfolio.id)
        if packages:
            for package in packages:
                Assertions.assert_true_raise400(not package.fare_id, translate(keyLanguage=language,
                                                                               keyToTranslate=
                                                                               "ERROR_FARE_PACKAGE_ALREADY_CREATED"))

        price_hour = json.get('priceHour')
        description = json.get('description')
        portfolio_id = logged_user.portfolio.id
        Assertions.assert_true_raise400(price_hour, translate(keyLanguage=language,
                                                              keyToTranslate="ERROR_PRICE_NOT_PROVIDED"))
        Assertions.assert_true_raise400(not check_is_number(request.data.get('priceHour')),
                                        translate(language, "ERROR_PRICEHOUR_CANT_BE_INTEGER"))
        Assertions.assert_true_raise400(not check_is_number(request.data.get('description')),
                                        translate(language, "ERROR_DESCRIPTION_CANT_BE_INTEGER"))

        Assertions.assert_true_raise400(isPositivefloat(price_hour) and float(price_hour) >= SystemConfiguration.objects.all().first().minimumPrice, translate(keyLanguage=language,
                                                                               keyToTranslate="ERROR_INVALID_PRICE"))


        fare = Fare.objects.create(priceHour=price_hour)
        PaymentPackage.objects.create(description=description,
                                      portfolio_id=portfolio_id, fare=fare)

        return fare

    @staticmethod
    def _service_update_package(json: dict, request, fare: Fare):
        language = check_accept_language(request)
        Assertions.assert_true_raise404(fare,
                                        translate(keyLanguage=language,
                                                  keyToTranslate="ERROR_FARE_PACKAGE_NOT_FOUND"))
        price_hour = json.get('priceHour')
        Assertions.assert_true_raise400(price_hour, translate(keyLanguage=language,
                                                              keyToTranslate="ERROR_PRICE_NOT_PROVIDED"))
        Assertions.assert_true_raise400(not check_is_number(request.data.get('priceHour')),
                                        translate(language, "ERROR_PRICEHOUR_CANT_BE_INTEGER"))
        Assertions.assert_true_raise400(not check_is_number(request.data.get('description')),
                                        translate(language, "ERROR_DESCRIPTION_CANT_BE_INTEGER"))
        Assertions.assert_true_raise400(isPositivefloat(price_hour) and float(price_hour) >= SystemConfiguration.objects.all().first().minimumPrice, translate(keyLanguage=language,
                                                                               keyToTranslate="ERROR_INVALID_PRICE"))

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

    def save(self, request, pk=None, logged_user=None):
        if pk is None:
            custom = self._service_create_package(self.initial_data, request, logged_user)
        else:
            custom = Custom.objects.filter(pk=pk).first()
            custom = self._service_update_package(self.initial_data, request, custom)
        return custom

    @staticmethod
    def _service_create_package(json: dict, request, logged_user):

        language = check_accept_language(request)
        packages = PaymentPackage.objects.filter(portfolio_id=logged_user.portfolio.id)
        if packages:
            for package in packages:
                Assertions.assert_true_raise400(not package.custom_id,
                                                translate(keyLanguage=language,
                                                          keyToTranslate="ERROR_CUSTOM_PACKAGE_ALREADY_CREATED"))

        minimum_price = json.get('minimumPrice')
        description = json.get('description')
        portfolio_id = logged_user.portfolio.id
        Assertions.assert_true_raise400(minimum_price, translate(keyLanguage=language,
                                                                 keyToTranslate="ERROR_MINIMUM_PRICE_NOT_PROVIDED"))

        Assertions.assert_true_raise400(isPositivefloat(minimum_price) and float(minimum_price) >= SystemConfiguration.objects.all().first().minimumPrice, translate(keyLanguage=language,
                                                                                  keyToTranslate="ERROR_INVALID_PRICE"))

        custom = Custom.objects.create(minimumPrice=minimum_price)
        PaymentPackage.objects.create(description=description,
                                      portfolio_id=portfolio_id, custom=custom)

        return custom

    @staticmethod
    def _service_update_package(json: dict, request, custom: Custom):
        language = check_accept_language(request)
        Assertions.assert_true_raise404(custom,
                                        translate(keyLanguage=language,
                                                  keyToTranslate="ERROR_CUSTOM_PACKAGE_NOT_FOUND"))
        minimumPrice = json.get('minimumPrice')
        Assertions.assert_true_raise400(minimumPrice,
                                        translate(keyLanguage=language,
                                                  keyToTranslate="ERROR_MINIMUM_PRICE_NOT_PROVIDED"))

        Assertions.assert_true_raise400(isPositivefloat(minimumPrice) and float(minimumPrice) >= SystemConfiguration.objects.all().first().minimumPrice,
                                        translate(keyLanguage=language,
                                                  keyToTranslate="ERROR_INVALID_PRICE"))

        custom.minimumPrice = json.get('minimumPrice')
        custom.paymentpackage.description = json.get('description')
        custom.save()
        return custom


class PerformanceSerializer(serializers.ModelSerializer):

    paymentPackage = PaymentPackageSerializer()

    class Meta:
        model = Performance
        fields = ('info', 'hours', 'price', 'paymentPackage')

    def save(self, request, pk=None, logged_user=None):

        if pk is None:
            performance = self._service_create_package(self.initial_data, request, logged_user)
        else:
            performance = Performance.objects.filter(pk=pk).first()
            performance = self._service_update_package(self.initial_data, request, performance)
        return performance

    @staticmethod
    def _service_create_package(json: dict, request, logged_user):
        language = check_accept_language(request)
        hours = json.get('hours')
        description = json.get('description')
        info = json.get('info')
        price = json.get('price')
        portfolio_id = logged_user.portfolio.id
        Assertions.assert_true_raise400(hours,
                                        translate(keyLanguage=language, keyToTranslate="ERROR_HOURS_NOT_PROVIDED"))
        Assertions.assert_true_raise400(info, translate(keyLanguage=language,
                                                        keyToTranslate="ERROR_INFO_NOT_PROVIDED"))
        Assertions.assert_true_raise400(price,
                                        translate(keyLanguage=language, keyToTranslate="ERROR_PRICE_NOT_PROVIDED"))

        Assertions.assert_true_raise400(isPositivefloat(hours), translate(keyLanguage=language,
                                                                          keyToTranslate="ERROR_INVALID_HOURS"))
        Assertions.assert_true_raise400(isPositivefloat(price) and float(price) >= SystemConfiguration.objects.all().first().minimumPrice, translate(keyLanguage=language,
                                                                          keyToTranslate="ERROR_INVALID_PRICE"))


        performance = Performance.objects.create(hours=hours, info=info, price=price)
        PaymentPackage.objects.create(description=description,
                                      portfolio_id=portfolio_id, performance=performance)

        return performance

    @staticmethod
    def _service_update_package(json: dict, request, performance: Performance):
        language = check_accept_language(request)
        Assertions.assert_true_raise404(performance,
                                        translate(keyLanguage=language,
                                                  keyToTranslate="ERROR_PERFORMANCE_PACKAGE_NOT_FOUND"))

        hours = json.get('hours')
        description = json.get('description')
        info = json.get('info')
        price = json.get('price')
        Assertions.assert_true_raise400(hours, translate(keyLanguage=language,
                                                         keyToTranslate="ERROR_HOURS_NOT_PROVIDED"))
        Assertions.assert_true_raise400(info, translate(keyLanguage=language,
                                                        keyToTranslate="ERROR_INFO_NOT_PROVIDED"))
        Assertions.assert_true_raise400(price, translate(keyLanguage=language,
                                                        keyToTranslate="ERROR_PRICE_NOT_PROVIDED"))
        Assertions.assert_true_raise400(isPositivefloat(hours), translate(keyLanguage=language,
                                                        keyToTranslate="ERROR_INVALID_HOURS"))
        Assertions.assert_true_raise400(isPositivefloat(price) and float(price) >= SystemConfiguration.objects.all().first().minimumPrice, translate(keyLanguage=language,
                                                             keyToTranslate="ERROR_INVALID_PRICE"))

        performance.hours = json.get('hours')
        performance.info = json.get('info')
        performance.price = json.get('price')
        performance.paymentpackage.description = description
        performance.save()
        return performance


