from Grooving.models import Offer, Customer
from utils.authentication_utils import get_logged_user, get_user_type, get_customer, get_artist
from rest_framework.response import Response
from rest_framework import generics
from .serializers import OfferSerializer, GetOfferSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from utils.Assertions import Assertions
from .serializers import translate
from utils.utils import check_accept_language
import pyqrcode


class OfferManage(generics.RetrieveUpdateDestroyAPIView):

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_object(self, pk=None):

        if pk is None:
            pk = self.kwargs['pk']

        language = check_accept_language(self.request)
        try:
            return Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            Assertions.assert_true_raise404(False,
                                            translate(language, 'ERROR_OFFER_NOT_FOUND'))

    def get(self, request, pk=None, format=None):

        language = check_accept_language(request)

        if pk is None:
            pk = self.kwargs['pk']
        offer = self.get_object(pk)
        articustomer = get_logged_user(request)
        user_type = get_user_type(articustomer)
        if user_type == "Artist":
            if articustomer.user_id == offer.paymentPackage.portfolio.artist.user_id:
                offer = self.get_object(pk)
                serializer = GetOfferSerializer(offer)
                return Response(serializer.data)
            else:
                Assertions.assert_true_raise403(False, translate(language, "ERROR_NOT_AN_ARTIST"))
        else:
            if user_type == "Customer":
                event_location = offer.eventLocation
                customer_id = event_location.customer_id
                customer_creator = Customer.objects.filter(pk=customer_id).first()

                if articustomer.user_id == customer_creator.user_id:
                    offer = self.get_object(pk)
                    serializer = OfferSerializer(offer)
                    return Response(serializer.data)
                else:
                    Assertions.assert_true_raise403(False, translate(language, "ERROR_NOT_A_CUSTOMER"))
            else:
                raise Assertions.assert_true_raise403(False, translate(language, "ERROR_NOT_LOGGED_IN"))

    def put(self, request, pk=None):

        language = check_accept_language(request)

        if pk is None:
            pk = self.kwargs['pk']
        if len(request.data) == 0:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            offer = self.get_object(pk)
            articustomer = get_logged_user(request)
            user_type = get_user_type(articustomer)
            if user_type == "Artist":
                if articustomer.user_id == offer.paymentPackage.portfolio.artist.user_id:
                    serializer = OfferSerializer(offer, data=request.data, partial=True)
                    serializer.save(pk, logged_user=articustomer, language=language)
                    return Response(status=status.HTTP_200_OK)
                else:
                    Assertions.assert_true_raise403(False, translate(language, "ERROR_NOT_AN_ARTIST"))
            else:
                if user_type == "Customer":
                    event_location = offer.eventLocation
                    customer_id = event_location.customer_id
                    customer_creator = Customer.objects.filter(pk=customer_id).first()

                    if articustomer.user_id == customer_creator.user_id:
                        serializer = OfferSerializer(offer, data=request.data, partial=True)
                        serializer.save(pk, logged_user=articustomer, language=language)
                        return Response(status=status.HTTP_200_OK)
                    else:
                        Assertions.assert_true_raise403(False, translate(language, "ERROR_NOT_A_CUSTOMER"))
                else:
                    Assertions.assert_true_raise403(False, translate(language, "ERROR_NOT_ALLOWED_USER"))

    def delete(self, request, pk=None, format=None):

        if pk is None:
            pk = self.kwargs['pk']
        offer = self.get_object(pk)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None, *args, **kwargs):

        if pk is None:
            pk = self.kwargs['pk']
        partial = kwargs.pop('partial', False)
        instance = self.get_object(pk)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)


class CreateOffer(generics.CreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request, *args, **kwargs):

        language = check_accept_language(request)

        serializer = OfferSerializer(data=request.data, partial=True)
        if serializer.validate(request):
            offer = serializer.save(logged_user=request.user, language=language)
            serialized = OfferSerializer(offer)
            return Response(serialized.data, status=status.HTTP_201_CREATED)


class NumOffers(generics.GenericAPIView):

    def get(self, request):

        language = check_accept_language(request)

        articustomer = get_logged_user(request)
        user_type = get_user_type(articustomer)

        if user_type == "Artist":
            numOffers = Offer.objects.filter(paymentPackage__portfolio__artist=articustomer, status='PENDING').count()
            return Response(numOffers, status=status.HTTP_200_OK)
        else:
            Assertions.assert_true_raise403(False, translate(language, "ERROR_USER_NOT_AUTHORIZED"))


class PaymentCode(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_object(self):
        offer_queryset = Offer.objects.filter(pk=self.request.query_params.get("offer", None))
        return offer_queryset

    def get(self, request, *args, **kwargs):

        language = check_accept_language(request)

        customer = get_customer(request)

        Assertions.assert_true_raise403(customer, translate(language, "ERROR_NOT_A_CUSTOMER"))
        offer = self.get_object().first()
        Assertions.assert_true_raise404(offer, translate(language, 'ERROR_CUSTOMER_NOT_FOUND'))
        Assertions.assert_true_raise403(offer.eventLocation.customer.id == customer.id,
                                        translate(language, 'ERROR_OFFER_NOT_OWNER'))

        return Response({"paymentCode": str(offer.paymentCode),
                         "qrcode": pyqrcode.create(offer.paymentCode).png_as_base64_str(scale=16)}, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        language = check_accept_language(request)

        offer = OfferSerializer.service_made_payment_artist(request.data.get("paymentCode"), get_artist(request), language=language)
        price = offer.price
        customer = offer.eventLocation.customer
        photo = customer.photo
        name = customer.user.first_name + " " + customer.user.last_name
        return Response({"offerId": offer.id, "price": price, "photo": photo, "name": name}, status=status.HTTP_200_OK)
