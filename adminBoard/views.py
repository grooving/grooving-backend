from rest_framework import generics
from django.utils import timezone
from datetime import datetime, timedelta
from Grooving.models import Artist, Customer, Offer
from rest_framework.response import Response
from utils.authentication_utils import get_admin, get_logged_user
from utils.Assertions import Assertions
from django.db.models import Sum


class GetRegisteredArtistsAllTime(generics.ListAPIView):

    #serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        artists = Artist.objects.all()

        return Response(len(artists))


class GetRegisteredCustomersAllTime(generics.ListAPIView):
    #serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):
        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})
        customers = Customer.objects.all()

        return Response(len(customers))


class GetPendingOffersAllTime(generics.ListAPIView):
    #serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        totaloffers = len(Offer.objects.all())

        pendingoffers = len(Offer.objects.filter(status='PENDING'))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = pendingoffers / totaloffers

            return Response(ratio)


class GetRejectedOffersAllTime(generics.ListAPIView):
    #serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        totaloffers = len(Offer.objects.all())

        rejectedoffers = len(Offer.objects.filter(status='REJECTED'))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = rejectedoffers / totaloffers

            return Response(ratio)


class GetContractMadeOffersAllTime(generics.ListAPIView):
    #serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        totaloffers = len(Offer.objects.all())

        contractoffers = len(Offer.objects.filter(status='CONTRACT_MADE'))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = contractoffers / totaloffers

            return Response(ratio)


class GetPaymentOffersAllTime(generics.ListAPIView):
    #serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        totaloffers = len(Offer.objects.all())

        paymentoffers = len(Offer.objects.filter(status='PAYMENT_MADE'))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = paymentoffers / totaloffers

            return Response(ratio)

class GetRegisteredArtistsLastMonth(generics.ListAPIView):

    #serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):
        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        time_threshold = datetime.now() - timedelta(hours=744)

        artists = Artist.objects.filter(creationMoment__gt=time_threshold)

        return Response(len(artists))


class GetRegisteredCustomersLastMonth(generics.ListAPIView):
    #serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):
        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        time_threshold = datetime.now() - timedelta(hours=744)

        customers = Customer.objects.filter(creationMoment__gt=time_threshold)

        return Response(len(customers))


class GetPendingOffersLastMonth(generics.ListAPIView):
    #serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        time_threshold = datetime.now() - timedelta(hours=744)
        totaloffers = len(Offer.objects.filter(creationMoment__gt=time_threshold))

        pendingoffers = len(Offer.objects.filter(status='PENDING').filter(creationMoment__gt=time_threshold))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = pendingoffers / totaloffers

            return Response(ratio)


class GetRejectedOffersLastMonth(generics.ListAPIView):
    #serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        time_threshold = datetime.now() - timedelta(hours=744)
        totaloffers = len(Offer.objects.filter(creationMoment__gt=time_threshold))

        rejectedoffers = len(Offer.objects.filter(status='REJECTED').filter(creationMoment__gt=time_threshold))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = rejectedoffers / totaloffers

            return Response(ratio)


class GetContractMadeOffersLastMonth(generics.ListAPIView):
    #serializer_class = ArtistInfoSerializer
    now = timezone.now()

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        #Se calcula un lapso de un mes
        time_threshold = datetime.now() - timedelta(hours=744)
        totaloffers = len(Offer.objects.filter(creationMoment__gt=time_threshold))
        #Se aplica un doble filtro para sacar las ofertas en este estado Y que sean del último mes (31 días en todos los casos, aun si tiene 30 días o es febrero)
        contractoffers = len(Offer.objects.filter(status='CONTRACT_MADE').filter(creationMoment__gt=time_threshold))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = contractoffers / totaloffers

            return Response(ratio)


class GetPaymentOffersLastMonth(generics.ListAPIView):
    # serializer_class = ArtistInfoSerializer
    now = timezone.now()

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        # Se calcula un lapso de un mes
        time_threshold = datetime.now() - timedelta(hours=744)
        totaloffers = len(Offer.objects.filter(creationMoment__gt=time_threshold))
        # Se aplica un doble filtro para sacar las ofertas en este estado Y que sean del último mes (31 días en todos los casos, aun si tiene 30 días o es febrero)
        paymentoffers = len(Offer.objects.filter(status='PAYMENT_MADE').filter(creationMoment__gt=time_threshold))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = paymentoffers / totaloffers

            return Response(ratio)


class GetTotalMoney(generics.ListAPIView):
    # serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        # Se calcula un lapso de un mes

        # Se aplica un doble filtro para sacar las ofertas en este estado Y que sean del último mes (31 días en todos los casos, aun si tiene 30 días o es febrero)
        paymentoffers = Offer.objects.filter(status='PAYMENT_MADE')
        totalPrice = 0.0

        for offer in paymentoffers:

            totalPrice = totalPrice + float(offer.price)

        return Response(totalPrice)


class GetMoneyEarned(generics.ListAPIView):
    # serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        # Se calcula un lapso de un mes

        # Se aplica un doble filtro para sacar las ofertas en este estado Y que sean del último mes (31 días en todos los casos, aun si tiene 30 días o es febrero)
        paymentoffers = Offer.objects.filter(status='PAYMENT_MADE')
        totalPrice = 0

        for offer in paymentoffers:

            totalPrice = totalPrice + float(offer.price)

        return Response(float(totalPrice)*0.07)


class GetTotalMoneyLastMonth(generics.ListAPIView):
    # serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        # Se calcula un lapso de un mes
        time_threshold = datetime.now() - timedelta(hours=744)
        # Se aplica un doble filtro para sacar las ofertas en este estado Y que sean del último mes (31 días en todos los casos, aun si tiene 30 días o es febrero)
        paymentoffers = Offer.objects.filter(status='PAYMENT_MADE').filter(creationMoment__gt=time_threshold)
        totalPrice = 0

        for offer in paymentoffers:

            totalPrice = totalPrice + float(offer.price)

        return Response(totalPrice)


class GetMoneyEarnedLastMonth(generics.ListAPIView):
    # serializer_class = ArtistInfoSerializer

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        # Se calcula un lapso de un mes
        time_threshold = datetime.now() - timedelta(hours=744)
        # Se aplica un doble filtro para sacar las ofertas en este estado Y que sean del último mes (31 días en todos los casos, aun si tiene 30 días o es febrero)
        paymentoffers = Offer.objects.filter(status='PAYMENT_MADE').filter(creationMoment__gt=time_threshold)
        totalPrice = 0

        for offer in paymentoffers:

            totalPrice = totalPrice + float(offer.price)

        return Response(float(totalPrice)*0.07)


class GetStatistics(generics.ListAPIView):

    def get(self, request, *args, **kwargs):

        #serializer_class =

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        totalArtists = GetRegisteredArtistsAllTime

        totalCustomers = GetRegisteredCustomersAllTime

        totalPendingOffers = GetPendingOffersAllTime

        totalRejectedOffers = GetRejectedOffersAllTime

        totalContractOffers = GetContractMadeOffersAllTime

        totalPaymentOffers = GetPaymentOffersAllTime

        successfulContractsMoney = GetTotalMoney

        moneyEarned = GetMoneyEarned

        totalArtistsLastMonth = GetRegisteredArtistsLastMonth

        totalCustomersLastMonth = GetRegisteredCustomersLastMonth

        totalPendingOffersLastMonth = GetPendingOffersLastMonth

        totalRejectedOffersLastMonth = GetRejectedOffersLastMonth

        totalContractOffersLastMonth = GetContractMadeOffersLastMonth

        totalPaymentOffersLastMonth = GetPaymentOffersLastMonth

        successfulContractsMoneyLastMonth = GetTotalMoneyLastMonth

        moneyEarnedLastMonth = GetMoneyEarnedLastMonth

        queryset = {'totalArtists': totalArtists, 'totalCustomers': totalCustomers}

        queryset = tuple(queryset)

        #queryset['totalArtists'] = totalArtists

        return Response(queryset)
