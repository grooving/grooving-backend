from django.shortcuts import render
from django.shortcuts import redirect, render
from Grooving.models import Offer,User,Customer
from django.contrib import messages
from django.db.utils import IntegrityError

from django.core.exceptions import PermissionDenied
from utils.authentication_utils import get_logged_user,get_user_type,is_user_authenticated
from rest_framework.response import Response
from rest_framework import generics
from .serializers import OfferSerializer
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

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

        if len(request.data) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:

            offer = self.get_object(pk)
            articustomer = get_logged_user(request)
            user_type = get_user_type(articustomer)
            if user_type == "Artist":
                if articustomer.user_id == offer.paymentPackage.portfolio.artist.user_id:
                    serializer = OfferSerializer(offer, data=request.data, partial=True)
                    serializer.save(pk)
                    return Response(status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied("The offer is not for yourself")
            else:
                if user_type == "Customer":
                    event_location = offer.eventLocation
                    customer_creator = Customer.objects.filter(eventLocation_id=event_location.id)

                    if articustomer.user_id == customer_creator.user_id:
                        serializer = OfferSerializer(offer, data=request.data, partial=True)
                        serializer.save(pk)
                        return Response(status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)


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


class CreateOffer(generics.CreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    #permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = OfferSerializer(data=request.data, partial=True)
        if serializer.validate(request):
            offer = serializer.save()
            serialized = OfferSerializer(offer)
            return Response(serialized.data, status=status.HTTP_201_CREATED)


class PaymentCode(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_object(self, pk):
        try:
            return Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        offer_id = request.GET.get("offer", None)
        offer = self.get_object(offer_id)
        serializer = OfferSerializer(offer)
        code = serializer.data.get("paymentCode")
        return Response({"paymentCode": str(code)}, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        paymentCode = request.data.get("paymentCode")
        if not paymentCode:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        OfferSerializer.service_made_payment_artist(paymentCode)
        return Response(status=status.HTTP_200_OK)
