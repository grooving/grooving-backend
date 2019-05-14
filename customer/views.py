from rest_framework.response import Response
from rest_framework import generics
from .serializers import CustomerInfoSerializer, PublicCustomerInfoSerializer
from Grooving.models import Customer
from utils.authentication_utils import get_user_type, get_logged_user
from rest_framework import status
from utils.Assertions import Assertions
from customer.serializers import CustomerSerializer
from customer.internationalization import translate
from utils.utils import check_accept_language


class GetPersonalInformationOfCustomer(generics.ListAPIView):
    serializer_class = CustomerInfoSerializer

    def get(self, request, *args, **kwargs):
        language = check_accept_language(request)

        user = get_logged_user(request)
        user_type = get_user_type(user)

        Assertions.assert_true_raise403(user is not None, translate(language, "ERROR_NOT_LOGGED_IN"))
        Assertions.assert_true_raise403(user_type == 'Customer', translate(language, "ERROR_NOT_A_CUSTOMER"))

        try:
            customer = Customer.objects.get(user_id=user.user_id)
            serializer = CustomerInfoSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            Assertions.assert_true_raise404(False, translate(language, "ERROR_NO_CUSTOMER_FOUND"))


class GetPublicInformationOfCustomer(generics.ListAPIView):
    serializer_class = PublicCustomerInfoSerializer

    def get_object(self, pk=None):
        language = check_accept_language(self.request)

        if pk is None:
            pk = self.kwargs['pk']
        language = check_accept_language(self.request)
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            Assertions.assert_true_raise404(False, translate(language, "ERROR_NO_CUSTOMER_FOUND"))

    def get(self, request, pk=None, format=None):
        language = check_accept_language(request)

        try:
            customer = self.get_object(pk)
            serializer = PublicCustomerInfoSerializer(customer)
            return Response(serializer.data)
        except Customer.DoesNotExist:
            Assertions.assert_true_raise404(False, translate(language, "ERROR_NO_CUSTOMER_FOUND"))


class CustomerRegister(generics.CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_object(self, pk=None):
        language = check_accept_language(self.request)
        check = self.request._request
        path = check.path_info
        if path == '/signupCustomer/':
            return {'Description': 'Method POST'}
        else:
            try:
                if pk is None:
                    pk = self.kwargs['pk']
                    if pk is not None:
                        return Customer.objects.get(pk=pk)
                    else:
                        Assertions.assert_true_raise404(False, translate(language, "ERROR_NO_CUSTOMER_FOUND"))
                else:
                    return Customer.objects.get(pk=pk)
            except:
                Assertions.assert_true_raise404(False, translate(language, "ERROR_NO_CUSTOMER_FOUND"))

    def post(self, request, *args, **kwargs):
        language = check_accept_language(request)

        Assertions.assert_true_raise400(len(request.data) != 0, translate(language, "ERROR_EMPTY_FORM"))
        user_type = None

        try:
            user = get_logged_user(request)
            user_type = get_user_type(user)
        except:
            pass
        if not user_type:
            serializer = CustomerSerializer(data=request.data, partial=True)
            if serializer.validate_customer(request):
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
        else:
            Assertions.assert_true_raise403(False, translate(language, "ERROR_MUST_LOGGED_OUT"))

    def put(self, request, pk=None):
        language = check_accept_language(request)

        if pk is None:
            pk = self.kwargs['pk']

        Assertions.assert_true_raise400(len(request.data) != 0, translate(language, "ERROR_EMPTY_FORM"))

        customer = Customer.objects.get(pk=pk)
        artist_or_customer = get_logged_user(request)
        Assertions.assert_true_raise403(artist_or_customer, translate(language, "ERROR_ARTIST_NOT_LOGGED"))
        Assertions.assert_true_raise403(artist_or_customer.id == customer.id,
                                        translate(language, "ERROR_IT_ISNT_YOUR_PERSONAL_INFO"))

        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        serializer.is_valid(True)
        customer = serializer.update(request, pk)

        customer.save()
        return Response(status=status.HTTP_200_OK)
