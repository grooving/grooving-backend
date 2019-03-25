from Grooving.models import Offer, Artist, Customer
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponseForbidden
from rest_framework import generics
from .serializers import ListOfferSerializer
from rest_framework.response import Response


class ListOffers(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ListOfferSerializer

    def get(self, name):
        print(self.request.user)

        if self.request.user.is_authenticated and not self.request.user.is_staff:
            try:
                artist = Artist.objects.get(user=self.request.user)
                queryset = Offer.objects.get(paymentPackage__portfolio__artist=artist)
                serializer = ListOfferSerializer(queryset)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                try:
                    customer = Customer.objects.get(user=self.request.user)
                    queryset = Offer.objects.get(eventLocation__customer=customer)
                    serializer = ListOfferSerializer(queryset)
                    return Response(serializer.data)
                except ObjectDoesNotExist:
                    return Response("You have no offers")
        else:
            raise PermissionDenied("No tienes autorización para entrar aquí")
