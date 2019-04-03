from Grooving.models import Offer, Customer,User,Artist,Portfolio
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.http import Http404
from utils.authentication_utils import get_user_type, get_logged_user
from .serializers import CustomerSerializer, ArtistSerializer
from utils.Assertions import Assertions


class ArtistManager(generics.CreateAPIView):

    serializer_class = ArtistSerializer

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

   
class CustomerManager(generics.CreateAPIView):

    serializer_class = CustomerSerializer

    
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
