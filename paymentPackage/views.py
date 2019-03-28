from django.shortcuts import render
from django.shortcuts import redirect, render
from Grooving.models import PaymentPackage,Artist
from django.contrib import messages
from django.db.utils import IntegrityError

from rest_framework.response import Response
from django.shortcuts import render_to_response
from rest_framework import generics
from .serializers import PaymentPackageSerializer
from rest_framework import status
from django.http import Http404


class PaymentPackageByArtist(generics.RetrieveUpdateDestroyAPIView):

    queryset = PaymentPackage.objects.all()
    serializer_class = PaymentPackageSerializer

    def get_object(self, pk):
        try:
            portfolio = Artist.objects.get(id=pk).portfolio
            return PaymentPackage.objects.filter(portfolio=portfolio)
        except PaymentPackage.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        portfolio = Artist.objects.get(id=pk).portfolio
        paymentPackage = PaymentPackage.objects.filter(portfolio=portfolio)
        serializer = PaymentPackageSerializer(paymentPackage, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        id_portfolio = Artist.objects.get(pk=pk).portfolio
        paymentPackage = self.get_object(portfolio__exact=id_portfolio)
        if len(request.data) == 1 and 'status' in request.data:
            serializer = PaymentPackageSerializer(paymentPackage, data=request.data, partial=True)

        else:
            serializer = PaymentPackageSerializer(paymentPackage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        id_portfolio = Artist.objects.get(pk=pk).portfolio
        paymentPackage = self.get_object(portfolio__exact=id_portfolio)
        paymentPackage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentPackageManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = PaymentPackage.objects.all()
    serializer_class = PaymentPackageSerializer

    def get_object(self, pk):
        try:
            return PaymentPackage.objects.get(pk=pk)
        except PaymentPackage.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        paymentPackage = PaymentPackage.objects.get(pk=pk)
        serializer = PaymentPackageSerializer(paymentPackage)
        return Response(serializer.data)

    def put(self, request, pk):
        paymentPackage = self.get_object(pk=pk)
        if len(request.data) == 1 and 'status' in request.data:
            serializer = PaymentPackageSerializer(paymentPackage, data=request.data, partial=True)

        else:
            serializer = PaymentPackageSerializer(paymentPackage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        paymentPackage = self.get_object(pk=pk)
        paymentPackage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreatePaymentPackage(generics.CreateAPIView):
    queryset = PaymentPackage.objects.all()
    serializer_class = PaymentPackageSerializer

    def post(self, request, *args, **kwargs):
        serializer = PaymentPackageSerializer(data=request.data, partial=True)
        if serializer.validate(request.data):
            serializer.is_valid()
            paymentPackage = serializer.save()
            serialized = PaymentPackageSerializer(paymentPackage)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

