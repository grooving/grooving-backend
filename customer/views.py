from rest_framework.response import Response
from rest_framework import generics
from .serializers import CustomerInfoSerializer
from django.core.exceptions import PermissionDenied
from Grooving.models import Customer
from utils.authentication_utils import get_user_type, get_logged_user, is_user_authenticated
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
