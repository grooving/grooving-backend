from rest_framework.response import Response
from rest_framework import generics,status
from .serializers import CustomerInfoSerializer, PublicCustomerInfoSerializer, CustomerSerializer
from django.core.exceptions import PermissionDenied
from Grooving.models import Customer
from utils.authentication_utils import get_user_type, get_logged_user, is_user_authenticated
from django.http import Http404
from rest_framework import status
from utils.Assertions import Assertions
from customer.serializers import CustomerSerializer


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


class CustomerRegister(generics.CreateAPIView):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_object(self, pk=None):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404

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

    def put(self, request, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        if len(request.data) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            customer = Customer.objects.get(pk=pk)
            articustomer = get_logged_user(request)

            Assertions.assert_true_raise403(articustomer.id == customer.id, "You can only change your personal info")
            serializer = CustomerSerializer(customer, data=request.data, partial=True)
            Assertions.assert_true_raise400(serializer.is_valid(), {"code": "invalid data"})
            customer = serializer.update(pk)

            customer.save()
            return Response(status=status.HTTP_200_OK)