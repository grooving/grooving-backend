from Grooving.models import User, Artist, Customer, Portfolio, PortfolioModule, Calendar, EventLocation, Admin
from utils.Assertions import Assertions
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import UserSerializer


class UserManage(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request):
        serializer = UserSerializer(data=request.data, partial=True)
        if serializer.validate_ban_user(request):
            user = User.objects.get(id=serializer.initial_data.get('id'))
            user.is_active = not user.is_active
            user.save()
            serialized = UserSerializer(user)
            return Response(serialized.data, status=status.HTTP_200_OK)
        else:
            Assertions.assert_true_raise400(False, {'error': 'ERROR_VALIDATE'})
