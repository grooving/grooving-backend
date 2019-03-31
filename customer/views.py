from rest_framework.response import Response
from rest_framework import generics
from .serializers import CustomerInfoSerializer, PublicCustomerInfoSerializer
from django.core.exceptions import PermissionDenied
from Grooving.models import Customer
from utils.authentication_utils import get_user_type, get_logged_user, is_user_authenticated
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist


class GetPersonalInformationOfCustomer(generics.ListAPIView):

    serializer_class = CustomerInfoSerializer

    def get(self, request, *args, **kwargs):

        user = get_logged_user(request)
        user_type = get_user_type(user)
        if user_type == 'Customer':
            customer = Customer.objects.get(user_id=user.user_id)
            serializer = CustomerInfoSerializer(customer)
            return Response(serializer.data)
        else:
            raise PermissionDenied()


class GetPublicInformationOfCustomer(generics.ListAPIView):

    serializer_class = PublicCustomerInfoSerializer

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

        try:
            customer = self.get_object(pk)
            serializer = PublicCustomerInfoSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            raise Http404
