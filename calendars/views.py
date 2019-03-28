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


class CalendarByArtist(generics.RetrieveUpdateDestroyAPIView):

    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def get_object(self, pk):
        try:
            portfolio = Artist.objects.get(id=pk).portfolio
            return Calendar.objects.get(portfolio=portfolio)
        except Calendar.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        portfolio = Artist.objects.get(id=pk).portfolio
        calendar = Calendar.objects.filter(portfolio=portfolio)
        serializer = CalendarSerializer(calendar, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        portfolio = self.get_object(pk)
        if len(request.data) == 1 and 'status' in request.data:
            serializer = CalendarSerializer(portfolio, data=request.data, partial=True)

        else:
            serializer = CalendarSerializer(portfolio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        portfolio = self.get_object(pk)
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)


class CalendarManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def get_object(self, pk):
        try:
            return Calendar.objects.get(pk=pk)
        except Calendar.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        calendar = Calendar.objects.get(pk=pk)
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)

    def put(self, request, pk):
        calendar = self.get_object(pk=pk)
        if len(request.data) == 1 and 'status' in request.data:
            serializer = CalendarSerializer(calendar, data=request.data, partial=True)

        else:
            serializer = CalendarSerializer(calendar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        calendar = self.get_object(pk=pk)
        calendar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateCalendar(generics.CreateAPIView):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def post(self, request, *args, **kwargs):
        serializer = CalendarSerializer(data=request.data, partial=True)
        if serializer.validate(request.data):
            serializer.is_valid()
            calendar = serializer.save()
            serialized = CalendarSerializer(calendar)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
