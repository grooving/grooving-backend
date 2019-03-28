from django.shortcuts import render
from django.shortcuts import redirect, render
from Grooving.models import PortfolioModule
from django.contrib import messages
from django.db.utils import IntegrityError

from rest_framework.response import Response
from django.shortcuts import render_to_response
from rest_framework import generics
from .serializers import PortfolioModuleSerializer
from rest_framework import status
from django.http import Http404


class PortfolioModuleManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = PortfolioModule.objects.all()
    serializer_class = PortfolioModuleSerializer

    def get_object(self, pk):
        try:
            return PortfolioModule.objects.get(pk=pk)
        except PortfolioModule.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        portfolioModule = PortfolioModule.objects.get(pk=pk)
        serializer = PortfolioModuleSerializer(portfolioModule)
        return Response(serializer.data)

    def put(self, request, pk):
        portfolioModule = self.get_object(pk=pk)
        if len(request.data) == 1 and 'status' in request.data:
            serializer = PortfolioModuleSerializer(portfolioModule, data=request.data, partial=True)

        else:
            serializer = PortfolioModuleSerializer(portfolioModule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        portfolioModule = self.get_object(pk=pk)
        portfolioModule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreatePortfolioModule(generics.CreateAPIView):
    queryset = PortfolioModule.objects.all()
    serializer_class = PortfolioModuleSerializer

    def post(self, request, *args, **kwargs):
        serializer = PortfolioModuleSerializer(data=request.data, partial=True)
        if serializer.validate(request.data):
            serializer.is_valid()
            portfolioModule = serializer.save()
            serialized = PortfolioModuleSerializer(portfolioModule)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
