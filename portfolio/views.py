from Grooving.models import Portfolio, Artist
from utils.authentication_utils import get_logged_user, get_user_type
from rest_framework.response import Response
from rest_framework import generics
from .serializers import PortfolioSerializer
from rest_framework import status
from django.http import Http404
from utils.Assertions import Assertions


class PortfolioManager(generics.RetrieveUpdateDestroyAPIView):

    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return Portfolio.objects.get(pk=pk)
        except Portfolio.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        portfolio = self.get_object(pk)
        serializer = PortfolioSerializer(portfolio, partial=True)
        return Response(serializer.data)

    def put(self, request, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        if Portfolio.objects.filter(pk=pk).first():
            portfolio = Portfolio.objects.filter(pk=pk).first()
            loggedUser = get_logged_user(request)
            user_type = get_user_type(loggedUser)
            artist = Artist.objects.filter(portfolio=portfolio).first()
            if loggedUser is not None and loggedUser.id == artist.id and user_type == "Artist":
                serializer = PortfolioSerializer(portfolio, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(loggedUser)
                    portfolio = self.get_object(pk)
                    serializer = PortfolioSerializer(portfolio, data=serializer.data, partial=True)
                    serializer.is_valid()
                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise Assertions.assert_true_raise403(False, {'error': 'Not logged or not owner of Portfolio'})
        else:
            return Assertions.assert_true_raise404(False)

    def delete(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        portfolio = self.get_object(pk)
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



