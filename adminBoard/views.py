from rest_framework import generics
from django.utils import timezone
from datetime import datetime, timedelta
from Grooving.models import Artist, Customer, Offer
from rest_framework.response import Response
from utils.authentication_utils import get_admin, get_logged_user
from utils.Assertions import Assertions
from django.db.models import Sum





class GetStatistics(generics.ListAPIView):

    def get_artists(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        artists = Artist.objects.all()

        return len(artists)

    def get_registered_customers_all_time(self, request, *args, **kwargs):
        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})
        customers = Customer.objects.all()

        return len(customers)

    def get_pending_offers_all_time(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        totaloffers = len(Offer.objects.all())

        pendingoffers = len(Offer.objects.filter(status='PENDING'))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = pendingoffers / totaloffers

            return ratio

    def get_rejected_offers_all_time(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        totaloffers = len(Offer.objects.all())

        rejectedoffers = len(Offer.objects.filter(status='REJECTED'))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = rejectedoffers / totaloffers

            return ratio

    def get_contract_made_offers_all_time(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        totaloffers = len(Offer.objects.all())

        contractoffers = len(Offer.objects.filter(status='CONTRACT_MADE'))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = contractoffers / totaloffers

            return ratio

    def get_payment_offers_all_time(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        totaloffers = len(Offer.objects.all())

        paymentoffers = len(Offer.objects.filter(status='PAYMENT_MADE'))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = paymentoffers / totaloffers

            return ratio

    def get_registered_artists_last_month(self, request, *args, **kwargs):
        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        time_threshold = datetime.now() - timedelta(hours=744)

        artists = Artist.objects.filter(creationMoment__gt=time_threshold)

        return len(artists)

    def get_registered_customers_last_month(self, request, *args, **kwargs):
        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        time_threshold = datetime.now() - timedelta(hours=744)

        customers = Customer.objects.filter(creationMoment__gt=time_threshold)

        return len(customers)

    def get_pending_offers_last_month(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        time_threshold = datetime.now() - timedelta(hours=744)
        totaloffers = len(Offer.objects.filter(creationMoment__gt=time_threshold))

        pendingoffers = len(Offer.objects.filter(status='PENDING').filter(creationMoment__gt=time_threshold))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = pendingoffers / totaloffers

            return ratio

    def get_rejected_offers_last_month(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        time_threshold = datetime.now() - timedelta(hours=744)
        totaloffers = len(Offer.objects.filter(creationMoment__gt=time_threshold))

        rejectedoffers = len(Offer.objects.filter(status='REJECTED').filter(creationMoment__gt=time_threshold))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = rejectedoffers / totaloffers

            return ratio

    def get_contract_made_offers_last_month(self, request, *args, **kwargs):
        now = timezone.now()
        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

            # Se calcula un lapso de un mes
        time_threshold = datetime.now() - timedelta(hours=744)
        totaloffers = len(Offer.objects.filter(creationMoment__gt=time_threshold))
            # Se aplica un doble filtro para sacar las ofertas en este estado Y que sean del último mes (31 días en todos los casos, aun si tiene 30 días o es febrero)
        contractoffers = len(
            Offer.objects.filter(status='CONTRACT_MADE').filter(creationMoment__gt=time_threshold))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = contractoffers / totaloffers

            return ratio

    def get_payment_offers_last_month(self, request, *args, **kwargs):

        admin = get_admin(request)
        now = timezone.now()
        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

            # Se calcula un lapso de un mes
        time_threshold = datetime.now() - timedelta(hours=744)
        totaloffers = len(Offer.objects.filter(creationMoment__gt=time_threshold))
            # Se aplica un doble filtro para sacar las ofertas en este estado Y que sean del último mes (31 días en todos los casos, aun si tiene 30 días o es febrero)
        paymentoffers = len(
            Offer.objects.filter(status='PAYMENT_MADE').filter(creationMoment__gt=time_threshold))

        if totaloffers == 0:

            return 0.0

        else:

            ratio = paymentoffers / totaloffers

            return ratio

    def get_total_money(self, request, *args, **kwargs):
        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

            # Se calcula un lapso de un mes

            # Se aplica un doble filtro para sacar las ofertas en este estado Y que sean del último mes (31 días en todos los casos, aun si tiene 30 días o es febrero)
        paymentoffers = Offer.objects.filter(status='PAYMENT_MADE')
        totalPrice = 0.0

        for offer in paymentoffers:
            totalPrice = totalPrice + float(offer.price)

        return totalPrice

    def get_money_earned(self, request, *args, **kwargs):
        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

            # Se calcula un lapso de un mes

            # Se aplica un doble filtro para sacar las ofertas en este estado Y que sean del último mes (31 días en todos los casos, aun si tiene 30 días o es febrero)
        paymentoffers = Offer.objects.filter(status='PAYMENT_MADE')
        totalPrice = 0

        for offer in paymentoffers:
            totalPrice = totalPrice + float(offer.price)

        return float(totalPrice) * 0.07

    def get_total_money_last_month(self, request, *args, **kwargs):
        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

            # Se calcula un lapso de un mes
        time_threshold = datetime.now() - timedelta(hours=744)
            # Se aplica un doble filtro para sacar las ofertas en este estado Y que sean del último mes (31 días en todos los casos, aun si tiene 30 días o es febrero)
        paymentoffers = Offer.objects.filter(status='PAYMENT_MADE').filter(creationMoment__gt=time_threshold)
        totalPrice = 0

        for offer in paymentoffers:
            totalPrice = totalPrice + float(offer.price)

        return totalPrice

    def get_money_earned_last_month(self, request, *args, **kwargs):
        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        # Se calcula un lapso de un mes
        time_threshold = datetime.now() - timedelta(hours=744)
        # Se aplica un doble filtro para sacar las ofertas en este estado Y que sean del último mes (31 días en todos los casos, aun si tiene 30 días o es febrero)
        paymentoffers = Offer.objects.filter(status='PAYMENT_MADE').filter(creationMoment__gt=time_threshold)
        totalPrice = 0

        for offer in paymentoffers:
            totalPrice = totalPrice + float(offer.price)

        return float(totalPrice) * 0.07
        #serializer_class =

    def get(self, request, *args, **kwargs):

        admin = get_admin(request)

        Assertions.assert_true_raise403(admin, {'error': 'ERROR_NOT_AN_ADMIN'})

        queryset = {}

        queryset['totalArtists'] = self.get_artists(request)

        queryset['totalCustomers'] = self.get_registered_customers_all_time(request)

        queryset['totalPendingOffers'] = self.get_pending_offers_all_time(request)

        queryset['totalRejectedOffers'] = self.get_rejected_offers_all_time(request)

        queryset['totalContractOffers'] = self.get_contract_made_offers_all_time(request)

        queryset['totalPaymentOffers'] = self.get_payment_offers_all_time(request)

        queryset['successfulContractsMoney'] = self.get_total_money(request)

        queryset['moneyEarned'] = self.get_money_earned(request)

        queryset['totalArtistsLastMonth'] = self.get_registered_artists_last_month(request)

        queryset['totalCustomersLastMonth'] = self.get_registered_customers_last_month(request)

        queryset['totalPendingOffersLastMonth'] = self.get_pending_offers_last_month(request)

        queryset['totalRejectedOffersLastMonth'] = self.get_rejected_offers_last_month(request)

        queryset['totalContractOffersLastMonth'] = self.get_contract_made_offers_last_month(request)

        queryset['totalPaymentOffersLastMonth'] = self.get_payment_offers_last_month(request)

        queryset['successfulContractsMoneyLastMonth'] = self.get_total_money_last_month(request)

        queryset['moneyEarnedLastMonth'] = self.get_money_earned_last_month(request)

        return Response(queryset)
