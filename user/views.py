from Grooving.models import User, Artist, Customer, Portfolio, PortfolioModule, Calendar, EventLocation, Admin,\
    UserAbstract
from utils.Assertions import Assertions
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import UserSerializer, ListArtistSerializer, PublicCustomerInfoSerializer
from utils.searcher.searcher import searchAdmin
from utils.authentication_utils import get_admin
from utils.notifications.notifications import Notifications


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
            return Response({'error': 'ERROR_VALIDATE'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            email = ''
            language = ''
            if Artist.objects.filter(user=request.user).first() is not None:
                artist = Artist.objects.get(user=request.user)
                UserSerializer.anonymize_and_hide_artist(artist)
                email = artist.user.email
                language = artist.language
            elif Customer.objects.filter(user=request.user).first() is not None:
                customer = Customer.objects.get(user=request.user)
                UserSerializer.anonymize_and_hide_customer(customer)
                email = customer.user.email
                language = customer.language
            else:
                Assertions.assert_true_raise400(False, {'error': 'ERROR_DELETE_USER_UNKNOWN'})
            request.user.delete()

            Notifications.send_email_right_to_be_forgotten(email=email, language=language)
        except TypeError:
            return Response({'error': 'ERROR_DELETE_USER'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListUsers(generics.RetrieveAPIView):

    serializer_class = ListArtistSerializer

    def get_queryset(self):

        return ['Something', ]

    def get(self, request, *args, **kwargs):
        admin = get_admin(request)
        Assertions.assert_true_raise403(admin is not None, {"error": "You are not admin"})
        username = request.query_params.get("username", None)
        #Assertions.assert_true_raise403()
        users = searchAdmin(username)
        artists = users.get("artists")
        customers = users.get("customers")
        dataUsers = []
        if artists:
            dataUsers = ListArtistSerializer(artists, many=True).data
            if customers:
                dataUsers.extend(PublicCustomerInfoSerializer(customers, many=True).data)

        return Response(dataUsers, status=status.HTTP_200_OK)