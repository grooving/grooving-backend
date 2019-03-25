from django.shortcuts import render
from django.shortcuts import redirect, render
from Grooving.models import Offer
from django.contrib import messages
from django.db.utils import IntegrityError

from rest_framework.response import Response
from django.shortcuts import render_to_response
from rest_framework import generics
from .serializers import OfferSerializer
from rest_framework import status
from django.http import Http404
from django.core import serializers
from rest_framework.permissions import IsAuthenticated


class OfferManage(generics.RetrieveUpdateDestroyAPIView):

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    #permission_classes = (IsAuthenticated,)

    '''def accept_offer(self, request):
        offer_id = request.GET.get('offer_id')
        offer = Offer.objects.get(id=offer_id)
        'artist = Artist.objects.filter(request.user)'
        'paymentpackage_id = offer.paymentPackage.id'
        'portfolio = Portfolio.objects.get(pk=paymentpackage_id)'
        'if request.user.is_authenticated:'
        if offer.status == 'PENDING':
                try:
                    offer.status = 'CONTRACT_MADE'
                    offer.save()
                except IntegrityError as e:
                    return render_to_response({"message": e.message})

        else:
            messages.add_message(request, messages.ERROR, "The offer is not available to be accepted")

        return redirect('')'''

    def get_object(self, pk):
        try:
            return Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        offer = self.get_object(pk)
        serializer = OfferSerializer(offer)
        return Response(serializer.data)

    def put(self, request, pk):
        offer = self.get_object(pk)
        #if len(request.data) == 1 and 'status' in request.data:
            #partial=True es muy importante, sin ello no funciona la actualización parcial de datos
        serializer = OfferSerializer(offer, data=request.data, partial=True)

        #else:
        #    serializer = OfferSerializer(offer, data=request.data)
        #if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        offer = self.get_object(pk)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
    """
    def post(self, request):
        serializer = CreateOfferRequest(data=request.data)
        if serializer.is_valid():
            serializer.data.status = 'PENDING'
            if serializer.validated_data.paymentPackage.performance is not None:
                serializer.validated_data.hours = serializer.validated_data.paymentPackage.performance.hours
                serializer.validated_data.price = serializer.validated_data.paymentPackage.performance.price
            elif serializer.validated_data.paymentPackage.fare is not None:
                serializer.validated_data.price = serializer.validated_data.paymentPackage.fare.price * \
                                                  serializer.validated_data.hours
            serializer.validated_data.paymentCode = None
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """


class CreateOffer(generics.CreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def post(self, request, *args, **kwargs):
        serializer = OfferSerializer(data=request.data, partial=True)
        if serializer.validate(request.data):
            offer = serializer.save()
            serialized = OfferSerializer(offer)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

    """
    def post(self, request, *args, **kwargs):
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.data.status = 'PENDING'
            if serializer.validated_data.paymentPackage.performance is not None:
                serializer.validated_data.hours = serializer.validated_data.paymentPackage.performance.hours
                serializer.validated_data.price = serializer.validated_data.paymentPackage.performance.price
            elif serializer.validated_data.paymentPackage.fare is not None:
                serializer.validated_data.price = serializer.validated_data.paymentPackage.fare.price * \
                                                  serializer.validated_data.hours
            serializer.validated_data.paymentCode = None
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    """