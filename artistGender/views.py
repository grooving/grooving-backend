from Grooving.models import ArtisticGender

from django.core.exceptions import PermissionDenied
from utils.authentication_utils import get_logged_user,get_user_type
from rest_framework.response import Response
from rest_framework import generics
from .serializers import ArtisticGenderSerializer, ShortArtisticGenderSerializer
from rest_framework import status
from utils.Assertions import Assertions


class ArtisticGenderManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = ArtisticGender.objects.all()
    serializer_class = ArtisticGenderSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return ArtisticGender.objects.get(pk=pk)
        except ArtisticGender.DoesNotExist:
            raise Assertions.assert_true_raise404(False, {'error': 'Artistic gender not found'})

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        portfolio = self.get_object(pk)
        serializer = ArtisticGenderSerializer(portfolio)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        artisticGender = self.get_object(pk)
        loggedUser = get_logged_user(request)
        type = get_user_type(loggedUser)
        if loggedUser is not None and type == "Artist":
            serializer = ArtisticGenderSerializer(artisticGender, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied("The artisticGender is not for yourself")

    def delete(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        artisticGender = self.get_object(pk)
        artisticGender.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateArtisticGender(generics.CreateAPIView):
    queryset = ArtisticGender.objects.all()
    serializer_class = ArtisticGenderSerializer

    def post(self, request, *args, **kwargs):
        loggedUser = get_logged_user(request)
        type = get_user_type(loggedUser)
        if loggedUser is not None and type == "Artist":
            serializer = ArtisticGenderSerializer(data=request.data, partial=True)
            if serializer.validate(request.data):
                serializer.is_valid()
                artisticGender = serializer.save()
                serialized = ArtisticGenderSerializer(artisticGender)
                return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            raise PermissionDenied("The artisticGender is not for yourself")


class ListArtisticGenders(generics.RetrieveUpdateDestroyAPIView):

    queryset = ArtisticGender.objects.all()
    serializer_class = ArtisticGenderSerializer

    def get_object(self, pk=None):
        try:
            return ArtisticGender.objects.get(pk=pk)
        except ArtisticGender.DoesNotExist:
            raise Assertions.assert_true_raise404(False, {'error': 'Artistic gender not found'})

    def get(self, request, pk=None, format=None):

        artisticGenders = ArtisticGender.objects.all()
        serializer = ShortArtisticGenderSerializer(artisticGenders, many=True)
        return Response(serializer.data)