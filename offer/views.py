from Grooving.models import Offer, Customer
from django.core.exceptions import PermissionDenied
from utils.authentication_utils import get_logged_user,get_user_type
from rest_framework.response import Response
from rest_framework import generics
from .serializers import OfferSerializer,OfferCodeSerializer
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class OfferManage(generics.RetrieveUpdateDestroyAPIView):

    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get_object(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            return Offer.objects.get(pk=pk)
        except Offer.DoesNotExist:
            raise Http404

    def get(self, request, pk=None, format=None):
        if pk is None:
            pk = self.kwargs['pk']
        offer = self.get_object(pk)
        articustomer = get_logged_user(request)
        user_type = get_user_type(articustomer)
        if user_type == "Artist":
            if articustomer.user_id == offer.paymentPackage.portfolio.artist.user_id:
                offer = self.get_object(pk)
                serializer = OfferSerializer(offer)
                return Response(serializer.data)
            else:
                raise PermissionDenied
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
                    raise PermissionDenied
            else:
                raise PermissionDenied

    def put(self, request, pk=None):
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
                    serializer.save(pk,logged_user=articustomer)
                    return Response(status=status.HTTP_200_OK)
                else:
                    raise PermissionDenied("The offer is not for yourself")
            else:
                if user_type == "Customer":
                    event_location = offer.eventLocation
                    customer_id = event_location.customer_id
                    customer_creator = Customer.objects.filter(pk=customer_id).first()

                    if articustomer.user_id == customer_creator.user_id:
                        serializer = OfferSerializer(offer, data=request.data, partial=True)
                        serializer.save(pk,logged_user=articustomer)
                        return Response(status=status.HTTP_200_OK)
                    else:
                        return Response(status=status.HTTP_400_BAD_REQUEST)

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
        serializer = OfferSerializer(data=request.data, partial=True)
        if serializer.validate(request):
            offer = serializer.save()
            serialized = OfferSerializer(offer)
            return Response(serialized.data, status=status.HTTP_201_CREATED)


class PaymentCode(generics.RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferCodeSerializer

    def get_object(self):
        queryset=self.filter_queryset(self.get_queryset())
        try:
            obj=queryset.get(pk=self.request.user.offer_id)
            self.check_object_permissions(self.request,obj)
            return obj

        except Offer.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        user = get_logged_user(request)
        user_type = get_user_type(user)
        if not user_type or user_type != "Customer":
            raise PermissionDenied("Only customers can call this.")
        offer_id = request.GET.get("offer", None)
        offer = self.pepe(offer_id)
        if not offer.eventLocation.customer.id == user.id:
            raise PermissionDenied("You are a customer, but you are not the owner of this offer")
        serializer = OfferCodeSerializer(offer)
        code = serializer.data.get("paymentCode")
        return Response({"paymentCode": str(code)}, status.HTTP_200_OK)

    def put(self, request, pk=None, *args, **kwargs):
        if pk is None:
            pk = self.kwargs['pk']
        try:
            offer1 = Offer.objects.filter(paymentCode=pk).first()
            offer1.status = "PAYMENT_MADE"
            offer1.save()

        except:
            raise PermissionDenied()

        #OfferSerializer.service_made_payment_artist(, get_logged_user(request))
        return Response(status=status.HTTP_200_OK)
