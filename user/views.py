from Grooving.models import Offer, Customer,User,Artist,Portfolio
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.http import Http404
from utils.authentication_utils import get_user_type, get_logged_user
from .serializers import CustomerSerializer, ArtistSerializer
from utils.Assertions import Assertions


class ArtistManager(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ArtistSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        artist = self.get_object(pk)
        logged_artist = get_logged_user(request)
        Assertions.assert_true_raise403(logged_artist.user_id == artist.user.id)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user_type = None
        try:
            user = get_logged_user(request)
            user_type = get_user_type(user)
        except:
            pass
        if not user_type:
            serializer = ArtistSerializer(data=request.data, partial=True)
            if serializer.validate_artist(request):
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)

        else:
                raise PermissionDenied("You must be unlogged to do this action")

    def update(self, request, pk=None, *args, **kwargs):
        if pk is None:
            pk = self.kwargs['pk']
        partial = kwargs.pop('partial', False)
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)


class CustomerManager(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = CustomerSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        customer = self.get_object(pk)
        logged_customer = get_logged_user(request)
        Assertions.assert_true_raise403(logged_customer.id == customer.id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user_type = None
        try:
            user = get_logged_user(request)
            user_type = get_user_type(user)
        except:
            pass
        if not user_type:
            serializer = CustomerSerializer(data=request.data, partial=True)
            if serializer.validate_customer(request):
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)

        else:
                raise PermissionDenied("You must be unlogged to do this action")

    def update(self, request, pk=None, *args, **kwargs):
        if pk is None:
            pk = self.kwargs['pk']
        partial = kwargs.pop('partial', False)
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
