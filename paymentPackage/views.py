from django.shortcuts import render
from django.shortcuts import redirect, render
from Grooving.models import PaymentPackage,Artist,Custom,Performance,Fare
from django.contrib import messages
from django.db.utils import IntegrityError

from rest_framework.response import Response
from django.shortcuts import render_to_response
from rest_framework import generics
from .serializers import PaymentPackageSerializer,PaymentPackageListSerializer, PaymentPackageSerializerShort,FareSerializer,CustomSerializer,PerformanceSerializer
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied
from utils.authentication_utils import get_logged_user,get_user_type,is_user_authenticated


class PaymentPackageByArtist(generics.RetrieveUpdateDestroyAPIView):

    queryset = PaymentPackage.objects.all()
    serializer_class = PaymentPackageListSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            portfolio = Artist.objects.get(id=pk).portfolio
            return PaymentPackage.objects.filter(portfolio=portfolio)
        except PaymentPackage.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format = None):
        if pk is None:
            pk = self.kwargs['pk']
        portfolio = Artist.objects.get(id=pk).portfolio
        paymentPackage = PaymentPackage.objects.filter(portfolio=portfolio)
        serializer = PaymentPackageListSerializer(paymentPackage, many=True)
        return Response(serializer.data)


class PaymentPackageManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = PaymentPackage.objects.all()
    serializer_class = PaymentPackageSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return PaymentPackage.objects.get(pk=pk)
        except PaymentPackage.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        paymentPackage = PaymentPackage.objects.get(pk=pk)
        serializer = PaymentPackageSerializerShort(paymentPackage)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        paymentPackage = self.get_object(pk=pk)
        loggedUser = get_logged_user(request)
        artist = Artist.objects.filter(portfolio=paymentPackage.portfolio).first()
        if loggedUser is not None and loggedUser.id == artist.id:
            serializer = PaymentPackageSerializer(paymentPackage, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied("The artisticGender is not for yourself")

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
        loggedUser = get_logged_user(request)
        type = get_user_type(loggedUser)
        if loggedUser is not None and type == "Artist":
            serializer = PaymentPackageSerializer(data=request.data, partial=True)
            if serializer.validate(request.data):
                serializer.is_valid()
                if request.data["portfolio_id"] == loggedUser.portfolio_id:
                    paymentPackage = serializer.save()
                    serialized = PaymentPackageSerializer(paymentPackage)
                    return Response(serialized.data, status=status.HTTP_201_CREATED)
                else:
                    raise PermissionDenied("The artisticGender is not for yourself")
        else:
            raise PermissionDenied("The artisticGender is not for yourself")


class CreateCustomPackage(generics.CreateAPIView):
    queryset = Custom.objects.all()
    serializer_class = CustomSerializer

    def get_object(self, pk=None):
        try:
            return Custom.objects.get(pk=pk)
        except Custom.DoesNotExist:
            raise Http404

    def post(self, request,pk=None):
        user_type = None

        try:
            logged_user = get_logged_user(request)
            user_type = get_user_type(logged_user)
        except:
            pass
        if user_type == "Artist":
            serializer = CustomSerializer(data=request.data,partial=True)
            if serializer.is_valid:
                serializer.save(pk,logged_user=logged_user)
                return Response(status=status.HTTP_201_CREATED)

        else:
            raise PermissionDenied("You have no permissions to do this action")


class CreatePerformancePackage(generics.CreateAPIView):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

    def get_object(self, pk=None):
        try:
            return Performance.objects.get(pk=pk)
        except Performance.DoesNotExist:
            raise Http404

    def post(self, request,pk=None):
        user_type = None
        try:
            logged_user = get_logged_user(request)
            user_type = get_user_type(logged_user)
        except:
            pass
        if user_type == "Artist":
            serializer = PerformanceSerializer(data=request.data, partial=True)
            if serializer.is_valid:
                serializer.save(pk,logged_user=logged_user)
                return Response(status=status.HTTP_201_CREATED)

        else:
            raise PermissionDenied("You have no permissions to do this action")


class CreateFarePackage(generics.CreateAPIView):
    queryset = Fare.objects.all()
    serializer_class = FareSerializer

    def get_object(self, pk=None):
        try:
            return Fare.objects.get(pk=pk)
        except Fare.DoesNotExist:
            raise Http404

    def post(self, request, pk=None):
        user_type = None
        try:
            logged_user = get_logged_user(request)
            user_type = get_user_type(logged_user)
        except:
            pass
        if user_type == "Artist":
            serializer = FareSerializer(data=request.data, partial=True)
            if serializer.is_valid:
                serializer.save(pk, logged_user=logged_user)
                return Response(status=status.HTTP_201_CREATED)

        else:
            raise PermissionDenied("You have no permissions to do this action")


