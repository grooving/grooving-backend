from django.shortcuts import render
from django.shortcuts import redirect, render
from Grooving.models import Zone, Artist, Portfolio
from django.contrib import messages
from django.db.utils import IntegrityError
from rest_framework.response import Response
from django.shortcuts import render_to_response
from rest_framework import generics
from .serializers import ZoneSerializer, SearchZoneSerializer
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied
from utils.authentication_utils import get_logged_user,get_user_type,is_user_authenticated
from collections import defaultdict


class ZoneManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return Zone.objects.get(pk=pk)
        except Zone.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        zone = self.get_object(pk)
        serializer = ZoneSerializer(zone)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        zone = self.get_object(pk)
        loggedUser = get_logged_user(request)
        type = get_user_type(loggedUser)
        if loggedUser is not None and type == "Artist":
            serializer = ZoneSerializer(zone, data=request.data, partial=True)

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
        zone = self.get_object(pk)
        zone.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateZone(generics.CreateAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    def post(self, request, *args, **kwargs):
        loggedUser = get_logged_user(request)
        type = get_user_type(loggedUser)
        if loggedUser is not None and type == "Artist":
            serializer = ZoneSerializer(data=request.data, partial=True)
            if serializer.validate(request.data):
                serializer.is_valid()
                zone = serializer.save()
                serialized = ZoneSerializer(zone)
                return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            raise PermissionDenied("The artisticGender is not for yourself")


class ListZones(generics.ListAPIView):

    serializer_class = SearchZoneSerializer

    def get_queryset(self):

    #   Pillamos al padre de todos los padres (o a aquellos que ya no tengan padre)

        zones = Zone.objects.all()

        return zones
