from Grooving.models import User, Artist, Customer, Portfolio, PortfolioModule, Calendar, EventLocation
from django.core.exceptions import PermissionDenied
from utils.authentication_utils import get_user_type, get_customer, get_artist
from utils.Assertions import Assertions
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class UserManage(generics.DestroyAPIView):
    queryset = User.objects.all()
    # serializer_class = OfferSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def delete(self, request):
        try:
            if Artist.objects.filter(user=request.user).first() is not None:
                artist = Artist.objects.get(user=request.user)
                portfolio = Portfolio.objects.filter(artist=artist).update(isHidden=True)
                PortfolioModule.objects.filter(portfolio=portfolio).update(isHidden=True)
                Calendar.objects.filter(portfolio=portfolio).update(isHidden=True)
            elif Customer.objects.filter(user=request.user).first() is not None:
                customer = Customer.objects.get(user=request.user)
                EventLocation.objects.filter(customer=customer).update(isHidden=True)
            else:
                Assertions.assert_true_raise400(False, {'error': 'ERROR_DELETE_USER_UNKNOWN'})
            request.user.delete()
        except TypeError:
            Assertions.assert_true_raise401(False, {'error': 'ERROR_DELETE_USER'})
        return Response(status=status.HTTP_204_NO_CONTENT)