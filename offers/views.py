from Grooving.models import Offer, Artist, Customer
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponseForbidden
from rest_framework import generics
from .serializers import ListOfferSerializer
from rest_framework.response import Response


class ListOffers(generics.ListAPIView):

    serializer_class = ListOfferSerializer

    def get_queryset(self):

        if self.request.user.is_authenticated and not self.request.user.is_staff:
            try:
                artist = Artist.objects.get(user=self.request.user)
                queryset = Offer.objects.filter(paymentPackage__portfolio__artist=artist)
                serializer = ListOfferSerializer(queryset, many=True)
                return queryset
            except ObjectDoesNotExist:
                try:
                    customer = Customer.objects.get(user=self.request.user)
                    queryset = Offer.objects.filter(eventLocation__customer=customer)
                    serializer = ListOfferSerializer(queryset, many=True)
                    return queryset
                except ObjectDoesNotExist:
                    #There are no offers matching the users; therefore, they have no offers linked to them. An empty list is given
                    queryset = ()
                    serializer = ListOfferSerializer(queryset)
                    return queryset
        else:
            raise PermissionDenied("No tienes autorización para entrar aquí")
