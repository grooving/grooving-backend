from Grooving.models import PaymentPackage, Artist, Custom, Performance, Fare
from rest_framework.response import Response
from rest_framework import generics
from paymentPackage.serializers import PaymentPackageSerializer, PaymentPackageListSerializer, FareSerializer,\
    CustomSerializer, PerformanceSerializer
from .serializers import PaymentPackageSerializerShort
from rest_framework import status
from utils.authentication_utils import get_logged_user, get_user_type
from utils.Assertions import Assertions
from utils.utils import check_accept_language
from paymentPackage.internationalization import translate
from django.core.exceptions import ObjectDoesNotExist


class PaymentPackageByArtist(generics.RetrieveUpdateDestroyAPIView):

    queryset = PaymentPackage.objects.all()
    serializer_class = PaymentPackageListSerializer

    def get_object(self, pk=None):
        language = check_accept_language(self.request)
        if pk is None:
            pk = self.kwargs['pk']
        try:
            portfolio = Artist.objects.get(id=pk).portfolio
            return PaymentPackage.objects.filter(portfolio=portfolio)
        except PaymentPackage.DoesNotExist:
            raise Assertions.assert_true_raise404(False,
                                                  translate(language, "ERROR_PAYMENT_PACKAGE_NOT_FOUND"))
        except ObjectDoesNotExist:
            raise Assertions.assert_true_raise404(False,
                                                  translate(language, "ERROR_NO_ARTIST_FOUND"))

    def get(self, request, pk=None, format=None):
        language = check_accept_language(request)
        if pk is None:
            pk = self.kwargs['pk']
        user = get_logged_user(request)
        Assertions.assert_true_raise403(user is not None, translate(language, "ERROR_MUST_BE_LOGGED"))
        user_type = get_user_type(user)

        try:
            artist = Artist.objects.get(pk=pk)
            Assertions.assert_true_raise401((user_type == 'Customer' or user.user_id == artist.user_id),
                                            translate(keyLanguage=language,
                                                      keyToTranslate="ERROR_NOT_OWNER"))
            portfolio = Artist.objects.get(id=pk).portfolio
            paymentPackage = PaymentPackage.objects.filter(portfolio=portfolio)
            serializer = PaymentPackageListSerializer(paymentPackage, many=True)
            return Response(serializer.data)
        except PaymentPackage.DoesNotExist:
            raise Assertions.assert_true_raise404(False,
                                                  translate(keyLanguage=language,
                                                            keyToTranslate="ERROR_PAYMENT_PACKAGE_NOT_FOUND"))
        except ObjectDoesNotExist:
            raise Assertions.assert_true_raise404(False,
                                                  translate(language, "ERROR_NO_ARTIST_FOUND"))

class PaymentPackageManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = PaymentPackage.objects.all()
    serializer_class = PaymentPackageSerializer

    def get_object(self, pk=None):
        language = check_accept_language(self.request)
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return PaymentPackage.objects.get(pk=pk)
        except PaymentPackage.DoesNotExist:
            raise Assertions.assert_true_raise404(False,
                                                  translate(keyLanguage=language,
                                                            keyToTranslate="ERROR_PAYMENT_PACKAGE_NOT_FOUND"))

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        paymentPackage = self.get_object(pk=pk)
        serializer = PaymentPackageSerializerShort(paymentPackage)
        return Response(serializer.data)

    def put(self, request, pk=None):
        language = check_accept_language(request)
        if pk is None:
            pk = self.kwargs['pk']
        paymentPackage = self.get_object(pk=pk)
        loggedUser = get_logged_user(request)
        artist = Artist.objects.filter(portfolio=paymentPackage.portfolio).first()
        if loggedUser is not None and loggedUser.id == artist.id:
            serializer = PaymentPackageSerializer(paymentPackage, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(request)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Assertions.assert_true_raise404(False,
                                                  translate(keyLanguage=language,
                                                            keyToTranslate="ERROR_NOT_OWNER"))

    def delete(self, request, pk=None, format=None):

        if pk is None:
            pk = self.kwargs['pk']
        paymentPackage = self.get_object(pk=pk)
        paymentPackage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreatePaymentPackage(generics.CreateAPIView):
    queryset = PaymentPackage.objects.all()
    serializer_class = PaymentPackageSerializer

    def post(self, request, *args, **kwargs):
        language = check_accept_language(request)
        loggedUser = get_logged_user(request)
        type = get_user_type(loggedUser)
        if loggedUser is not None and type == "Artist":
            serializer = PaymentPackageSerializer(data=request.data, partial=True)
            if serializer.validate(request.data):
                serializer.is_valid()
                if request.data["portfolio_id"] == loggedUser.portfolio_id:
                    paymentPackage = serializer.save(request)
                    serialized = PaymentPackageSerializer(paymentPackage)
                    return Response(serialized.data, status=status.HTTP_201_CREATED)
                else:
                    raise Assertions.assert_true_raise404(False,
                                                          translate(keyLanguage=language,
                                                                    keyToTranslate="ERROR_NOT_OWNER"))
        else:
            raise Assertions.assert_true_raise404(False,
                                                  translate(keyLanguage=language,
                                                            keyToTranslate="ERROR_NOT_OWNER"))


class CreateCustomPackage(generics.CreateAPIView):
    queryset = Custom.objects.all()
    serializer_class = CustomSerializer

    def get_object(self, pk=None):
        language = check_accept_language(self.request)
        try:
            return Custom.objects.get(pk=pk)
        except Custom.DoesNotExist:
            Assertions.assert_true_raise404(False,
                                            translate(keyLanguage=language,
                                                      keyToTranslate="ERROR_CUSTOM_PACKAGE_NOT_FOUND"))

    def post(self, request, pk=None):
        language = check_accept_language(request)
        user_type = None

        try:
            logged_user = get_logged_user(request)
            Assertions.assert_true_raise403(logged_user is not None, translate(language, "ERROR_NOT_LOGGED_IN"))
            user_type = get_user_type(logged_user)
        except:
            pass

        if pk:
            package = PaymentPackage.objects.filter(custom_id=pk).first()
            Assertions.assert_true_raise404(package, translate(keyLanguage=language,
                                                               keyToTranslate="ERROR_CUSTOM_PACKAGE_NOT_FOUND"))
            owner = package.portfolio.artist
            Assertions.assert_true_raise403(logged_user.user.id == owner.user.id, translate(keyLanguage=language,
                                                            keyToTranslate="ERROR_CUSTOM_PACKAGE_NOT_OWNER"))

        if user_type == "Artist":
            serializer = CustomSerializer(data=request.data, partial=True)
            if serializer.is_valid:
                serializer.save(request, pk, logged_user=logged_user)
                return Response(status=status.HTTP_200_OK)

        else:
            raise Assertions.assert_true_raise404(False,
                                                  translate(keyLanguage=language,
                                                            keyToTranslate="ERROR_CUSTOM_PACKAGE_NOT_OWNER"))


class CreatePerformancePackage(generics.CreateAPIView):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

    def get_object(self, pk=None):
        language = check_accept_language(self.request)
        try:
            return Performance.objects.get(pk=pk)
        except Performance.DoesNotExist:
            Assertions.assert_true_raise404(False,
                                            translate(keyLanguage=language,
                                                      keyToTranslate="ERROR_PERFORMANCE_PACKAGE_NOT_FOUND"))

    def post(self, request,pk=None):
        language = check_accept_language(request)
        user_type = None
        try:
            logged_user = get_logged_user(request)
            Assertions.assert_true_raise403(logged_user is not None, translate(language, "ERROR_NOT_LOGGED_IN"))
            user_type = get_user_type(logged_user)
        except:
            pass

        if pk:
            package = PaymentPackage.objects.filter(performance_id=pk).first()

            Assertions.assert_true_raise404(package, translate(keyLanguage=language,
                                                      keyToTranslate="ERROR_PERFORMANCE_PACKAGE_NOT_FOUND"))

            owner = package.portfolio.artist
            Assertions.assert_true_raise403(logged_user.user.id == owner.user.id, translate(keyLanguage=language,
                                                            keyToTranslate="ERROR_PERFORMANCE_PACKAGE_NOT_OWNER"))

        if user_type == "Artist":
            serializer = PerformanceSerializer(data=request.data, partial=True)
            if serializer.is_valid:
                serializer.save(request, pk, logged_user)
                return Response(status=status.HTTP_200_OK)

        else:
            raise Assertions.assert_true_raise403(False,
                                                  translate(keyLanguage=language,
                                                            keyToTranslate="ERROR_PERFORMANCE_PACKAGE_NOT_OWNER"))


class CreateFarePackage(generics.CreateAPIView):
    queryset = Fare.objects.all()
    serializer_class = FareSerializer

    def get_object(self, pk=None):
        language = check_accept_language(self.request)
        try:
            return Fare.objects.get(pk=pk)
        except Fare.DoesNotExist:
            Assertions.assert_true_raise404(False,
                                            translate(keyLanguage=language,
                                                      keyToTranslate="ERROR_FARE_PACKAGE_NOT_FOUND"))

    def post(self, request, pk=None):
        language = check_accept_language(request)
        user_type = None

        logged_user = get_logged_user(request)
        Assertions.assert_true_raise403(logged_user is not None, translate(language, "ERROR_NOT_LOGGED_IN"))
        user_type = get_user_type(logged_user)

        if pk:
            package = PaymentPackage.objects.filter(fare_id=pk).first()
            Assertions.assert_true_raise404(package, translate(keyLanguage=language,
                                                               keyToTranslate="ERROR_FARE_PACKAGE_NOT_FOUND"))
            owner = package.portfolio.artist
            Assertions.assert_true_raise403(logged_user.user.id == owner.user.id, translate(keyLanguage=language,
                                                            keyToTranslate="ERROR_FARE_PACKAGE_NOT_OWNER"))

        if user_type == "Artist":
            serializer = FareSerializer(data=request.data, partial=True)
            if serializer.is_valid:
                serializer.save(request, pk, logged_user=logged_user)
                return Response(status=status.HTTP_200_OK)

        else:
            raise Assertions.assert_true_raise403(False,
                                                  translate(keyLanguage=language,
                                                            keyToTranslate="ERROR_FARE_PACKAGE_NOT_OWNER"))


