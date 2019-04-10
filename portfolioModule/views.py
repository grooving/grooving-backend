from Grooving.models import PortfolioModule, Artist
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PortfolioModuleSerializer
from rest_framework import status
from django.http import Http404
from django.core.exceptions import PermissionDenied
from utils.authentication_utils import get_logged_user,get_user_type,is_user_authenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PortfolioModuleManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = PortfolioModule.objects.all()
    serializer_class = PortfolioModuleSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return PortfolioModule.objects.get(pk=pk)
        except PortfolioModule.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        portfolioModule = PortfolioModule.objects.get(pk=pk)
        serializer = PortfolioModuleSerializer(portfolioModule)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        portfolioModule = self.get_object(pk=pk)
        loggedUser = get_logged_user(request)
        artist = Artist.objects.filter(portfolio=portfolioModule.portfolio).first()
        if loggedUser is not None and loggedUser.id == artist.id:
            serializer = PortfolioModuleSerializer(portfolioModule, data=request.data, partial=True)
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
        portfolioModule = self.get_object(pk=pk)
        portfolioModule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreatePortfolioModule(generics.CreateAPIView):
    queryset = PortfolioModule.objects.all()
    serializer_class = PortfolioModuleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):
        serializer = PortfolioModuleSerializer(data=request.data, partial=True)
        if serializer.validate(request):
            module = serializer.save(logged_user=request.user)
            serialized = PortfolioModuleSerializer(module)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
