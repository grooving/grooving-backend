from Grooving.models import EventLocation, Artist, Customer, Offer, Portfolio
from utils.authentication_utils import get_logged_user, get_user_type
from django.core.exceptions import PermissionDenied

from rest_framework.response import Response
from rest_framework import generics
from .serializers import EventLocationSerializer
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Create your views here.


class EventLocationManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = EventLocation.objects.all()
    serializer_class = EventLocationSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return EventLocation.objects.get(pk=pk)
        except EventLocation.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        eventLocation = self.get_object(pk)
        articustomer = get_logged_user(request)
        user_type = get_user_type(articustomer)
        if user_type == "Artist":
            offer = Offer.objects.all.filter(eventLocation_id=eventLocation.id)
            portfolio = Portfolio.objects.get(paymentPackage_id=offer.paymentPackage_id)
            artist = Artist.objects.get(portfolio_id=portfolio.id)
            if articustomer.user_id == artist.user_id:
                serializer = EventLocationSerializer(eventLocation)
                return Response(serializer.data)
            else:
                raise PermissionDenied
        elif user_type == "Customer":
            customer_id = eventLocation.customer_id
            customer_creator = Customer.objects.filter(pk=customer_id).first()
            if articustomer.user_id == customer_creator.user_id:
                serializer = EventLocationSerializer(eventLocation)
                return Response(serializer.data)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied


class CreateEventLocation(generics.CreateAPIView):
    queryset = EventLocation.objects.all()
    serializer_class = EventLocationSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        serializer = EventLocationSerializer(data=request.data, partial=True)
        if serializer.validate(request):
            eventLocation = serializer.save(request.user.id)
            serialized = EventLocationSerializer(eventLocation)
            return Response(serialized.data, status=status.HTTP_201_CREATED)

