from django.shortcuts import render
from django.shortcuts import redirect, render
from Grooving.models import Calendar,Portfolio,Artist
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
from utils.Assertions import Assertions


class CalendarByArtist(generics.RetrieveUpdateDestroyAPIView):

    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            artist = Artist.objects.get(id=pk)
            calendar= Calendar.objects.get(portfolio_id=artist.portfolio.id)
            return calendar
        except Calendar.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        artist = Artist.objects.get(id=pk)
        calendar = Calendar.objects.filter(portfolio_id=artist.portfolio.id)
        serializer = CalendarSerializer(calendar, many=True)
        return Response(serializer.data)


class CalendarManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return Calendar.objects.get(portfolio__artist__id=pk)
        except Calendar.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        calendar = Calendar.objects.filter(portfolio__artist__id=pk).first()
        Assertions.assert_true_raise404(calendar is not None, {'error': 'No calendar with that id'})
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        calendar = Calendar.objects.filter(portfolio__artist__id=pk).first()

        Assertions.assert_true_raise400(len(request.data) != 0, {'error': 'No fields were given'})
        Assertions.assert_true_raise400(calendar is not None, {'error': 'Calendar does not exist'})

        loggedUser = get_logged_user(request)
        artist = Artist.objects.filter(portfolio=calendar.portfolio).first()
        Assertions.assert_true_raise403(loggedUser is not None and loggedUser.id == artist.id, {'error': 'User Id does not match calendar owner'})
        serializer = CalendarSerializer(calendar, data=request.data, partial=True)
        Assertions.assert_true_raise400(serializer.is_valid(),{'error': 'Data in serializer is not valid'})
        serializer.save(pk,loggedUser)
        calendar = self.get_object(pk)

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        calendar = self.get_object(pk)
        calendar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateCalendar(generics.CreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def post(self, request, pk=None, **kwargs):
        loggedUser = get_logged_user(request)
        type = get_user_type(loggedUser)
        Assertions.assert_true_raise403(loggedUser is not None and type == "Artist", {'error': 'User is not an artist'})
        serializer = CalendarSerializer(data=request.data, partial=True)
        if serializer.validate(request.data):
            serializer.is_valid()
            Assertions.assert_true_raise403(request.data["portfolio"] == loggedUser.portfolio_id, {'error': 'You do not own this calendar'})
            calendar = serializer.save(pk,loggedUser)
            serialized = CalendarSerializer(calendar)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
