from django.shortcuts import render
from django.shortcuts import redirect, render
from Grooving.models import Calendar, Artist
from django.contrib import messages
from django.db.utils import IntegrityError

from rest_framework.response import Response
from django.shortcuts import render_to_response
from rest_framework import generics
from .serializers import CalendarSerializer
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied
from utils.authentication_utils import get_logged_user,get_user_type,is_user_authenticated


class CalendarByArtist(generics.RetrieveUpdateDestroyAPIView):

    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            portfolio = Artist.objects.get(id=pk).portfolio
            return Calendar.objects.get(portfolio=portfolio)
        except Calendar.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        portfolio = Artist.objects.get(id=pk).portfolio
        calendar = Calendar.objects.filter(portfolio=portfolio)
        serializer = CalendarSerializer(calendar, many=True)
        return Response(serializer.data)


class CalendarManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return Calendar.objects.get(pk=pk)
        except Calendar.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        calendar = self.get_object(pk)
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        calendar = self.get_object(pk)
        loggedUser = get_logged_user(request)
        artist = Artist.objects.filter(portfolio=calendar.portfolio).first()
        if loggedUser is not None and loggedUser.id == artist.id:
            serializer = CalendarSerializer(calendar, data=request.data, partial=True)

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
        calendar = self.get_object(pk)
        calendar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateCalendar(generics.CreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def post(self, request, *args, **kwargs):
        loggedUser = get_logged_user(request)
        type = get_user_type(loggedUser)
        if loggedUser is not None and type == "Artist":
            serializer = CalendarSerializer(data=request.data, partial=True)
            if serializer.validate(request.data):
                serializer.is_valid()
                if request.data["portfolio"] == loggedUser.portfolio_id:
                    calendar = serializer.save()
                    serialized = CalendarSerializer(calendar)
                    return Response(serialized.data, status=status.HTTP_201_CREATED)
                else:
                    raise PermissionDenied("The artisticGender is not for yourself")

        else:
            raise PermissionDenied("The artisticGender is not for yourself")
