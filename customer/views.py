from rest_framework.response import Response
from rest_framework import generics
from .serializers import CustomerInfoSerializer
from django.core.exceptions import PermissionDenied
from Grooving.models import Customer
from django.core.exceptions import ObjectDoesNotExist


class GetPersonalInformationOfCustomer(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = CustomerInfoSerializer

    def get(self, name):

        if self.request.user.is_authenticated:
            loggeduser = self.request.user
            try:
                queryset = Customer.objects.get(user=loggeduser)
                serializer = CustomerInfoSerializer(queryset)
                return Response(serializer.data)
            except ObjectDoesNotExist:
                raise PermissionDenied()
        else:
            raise PermissionDenied()
