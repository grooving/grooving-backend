from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status
from login.serializers import ArtistSerializer, CustomerSerializer, LoginSerializer
from django.contrib.auth.models import User
from Grooving.models import Artist, Customer, Admin


class LoginManager(ObtainAuthToken):
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    # serializer_class = UserSerializer

    def post(self, request):
        authTokenSerializer = AuthTokenSerializer(data=request.data)
        if authTokenSerializer.is_valid(raise_exception=True):
            user = authTokenSerializer.validated_data['user']
            last_login = user.last_login
            update_last_login(None, user)
            token, created = Token.objects.get_or_create(user=user)
            if token.key is not None:
                headers = {'x-auth': token.key}
                if Artist.objects.filter(user_id=token.user.id).first():
                    artist = Artist.objects.get(user_id=token.user.id)
                    artist.user.last_login = last_login
                    serialized = LoginSerializer(artist)
                elif Customer.objects.filter(user_id=token.user.id).first():
                    customer = Customer.objects.get(user_id=token.user.id)
                    customer.user.last_login = last_login
                    serialized = LoginSerializer(customer)
                # elif Admin.objects.filter(user_id=token.user.id).first():
                #     admin = Admin.objects.get(user_id=token.user.id)
                #     admin.user.last_login = last_login
                #     serialized = LoginSerializer(admin)
                else:
                    return Response({"User not found"}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serialized.data, status=status.HTTP_200_OK, headers=headers)
            else:
                return Response({"Token not get/created"}, status=status.HTTP_400_BAD_REQUEST)


class AdminLoginManager(ObtainAuthToken):
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    # serializer_class = UserSerializer

    def post(self, request):
        authTokenSerializer = AuthTokenSerializer(data=request.data)
        if authTokenSerializer.is_valid(raise_exception=True):
            user = authTokenSerializer.validated_data['user']
            last_login = user.last_login
            update_last_login(None, user)
            token, created = Token.objects.get_or_create(user=user)
            if token.key is not None:
                headers = {'x-auth': token.key}
                if Admin.objects.filter(user_id=token.user.id).first():
                    admin = Admin.objects.get(user_id=token.user.id)
                    admin.user.last_login = last_login
                    serialized = LoginSerializer(admin)
                else:
                    return Response({"Admin not found"}, status=status.HTTP_400_BAD_REQUEST)
                return Response(serialized.data, status=status.HTTP_200_OK, headers=headers)
            else:
                return Response({"Token not get/created"}, status=status.HTTP_400_BAD_REQUEST)
