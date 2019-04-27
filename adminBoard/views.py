from rest_framework import generics, status
from django.utils import timezone
from datetime import datetime, timedelta
from Grooving.models import Artist, Customer, Offer, Zone, EventLocation
from rest_framework.response import Response
from utils.authentication_utils import get_admin_2, get_admin
from utils.utils import check_accept_language
from utils.Assertions import Assertions
from adminBoard.serializers import ZoneSerializer
from adminBoard.internationalization import translate


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


class AdminZoneManagement(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ZoneSerializer

    def get(self, request, pk=None):
        language = check_accept_language(request)
        try:
            zone = Zone.objects.get(pk=pk)
            serializer = ZoneSerializer(zone)
            return Response(serializer.data)

        except Zone.DoesNotExist:
            Assertions.assert_true_raise404(False,
                                            translate(keyLanguage=language, keyToTranslate="ERROR_ZONE_NOT_FOUND"))

    def post(self, request):
        language = check_accept_language(request)
        Assertions.assert_true_raise400(len(request.data) != 0, translate(keyLanguage=language,
                                                                          keyToTranslate="ERROR_EMPTY_FORM_NOT_VALID"))
        admin = get_admin_2(request)

        Assertions.assert_true_raise403(admin, translate(keyLanguage=language,
                                                         keyToTranslate="ERROR_FORBIDDEN_NO_ADMIN"))
        serializer = ZoneSerializer(data=request.data, partial=True)
        if serializer.validate_zone(request):
            serializer.save(request)

            return Response(status=status.HTTP_201_CREATED)

        else:
            Assertions.assert_true_raise400(False, translate(keyLanguage=language,
                                                             keyToTranslate="ERROR_FORBIDDEN_NO_ADMIN"))

    def put(self, request, pk=None):
        language = check_accept_language(request)
        if pk is None:
            pk = self.kwargs['pk']
        Assertions.assert_true_raise400(len(request.data) != 0, translate(keyLanguage=language,
                                                                          keyToTranslate="ERROR_EMPTY_FORM_NOT_VALID"))
        language = check_accept_language(request)
        admin = get_admin_2(request)

        Assertions.assert_true_raise403(admin, translate(keyLanguage=language,
                                                         keyToTranslate="ERROR_FORBIDDEN_NO_ADMIN"))
        zone = Zone.objects.get(pk=pk)
        serializer = ZoneSerializer(zone, data=request.data, partial=True)

        if serializer.validate_zone(request):
            zone = serializer.update(request, pk)
            zone.save()

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        language = check_accept_language(request)
        pks = list(Zone.objects.values_list("id",flat=True))
        Assertions.assert_true_raise400(pk, translate(keyLanguage=language,
                                                        keyToTranslate="ERROR_ZONE_NOT_FOUND"))
        admin = get_admin_2(request)

        Assertions.assert_true_raise403(admin, translate(keyLanguage=language,
                                                         keyToTranslate="ERROR_FORBIDDEN_NO_ADMIN"))

        Assertions.assert_true_raise400(int(pk) in pks, translate(keyLanguage=language,
                                                                     keyToTranslate="ERROR_ZONE_NOT_FOUND"))
        zone = Zone.objects.get(id=pk)
        Assertions.assert_true_raise400(zone, translate(keyLanguage=language,
                                                        keyToTranslate="ERROR_ZONE_NOT_FOUND"))
        events = EventLocation.objects.all()
        parentzones= []

        for event in events:
            try:
                pzone = event.zone.parentZone
                zone1 = event.zone
                if pzone not in parentzones or zone1 not in parentzones:
                    parentzones.append(zone1)
                    parentzones.append(pzone)
            except:
                pass

        for parentzone in parentzones:

            try:
                pzone = parentzone.parentZone
                if pzone or pzone not in parentzones:
                    parentzones.append(pzone)
            except:
                continue

        Assertions.assert_true_raise400(not(zone in parentzones), translate(keyLanguage=language,
                                                        keyToTranslate="ERROR_ZONE_BELONGS_TO_EVENT"))
        zone.delete()
        return Response(status=status.HTTP_200_OK)


