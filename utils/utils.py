from django.utils import timezone
from Grooving.models import SystemConfiguration
from rest_framework import generics
from rest_framework.response import Response
import utils.Assertions
from utils.Assertions import Assertions
from utils.authentication_utils import get_admin
from utils.notifications.notifications import Notifications


def auto_update_old_offers(offers):
    now = timezone.now()
    if not offers:
        pass
    if len(offers) == 0:
        pass
    else:
        for o in offers:
            if o.status == 'PENDING' and o.date < now:
                o.status = 'REJECTED'
                o.save()


def cancel_offers_with_no_user(offers):

    if not offers:
        pass
    if len(offers) == 0:
        pass
    else:
        for o in offers:
            if o.status != 'PAYMENT_MADE' and (o.paymentPackage.portfolio.isHidden or o.eventLocation.isHidden):
                o.status = 'REJECTED'
                o.save()


class TermsAndConditions(generics.GenericAPIView):

    @staticmethod
    def get(request):
        language = request.META['HTTP_ACCEPT_LANGUAGE']
        result = None
        print(language)

        if language.find("en") != -1:
            result = SystemConfiguration.objects.all().first().termsText_en
        elif language.find("es") != -1:
            result = SystemConfiguration.objects.all().first().termsText_es

        return Response(result)


class Privacy(generics.GenericAPIView):

    @staticmethod
    def get(request):
        language = request.META['HTTP_ACCEPT_LANGUAGE']
        result = None
        print(language)

        if language.find("en") != -1:
            result = SystemConfiguration.objects.all().first().privacyText_en
        elif language.find("es") != -1:
            result = SystemConfiguration.objects.all().first().privacyText_es

        return Response(result)


class AboutUs(generics.GenericAPIView):

    @staticmethod
    def get(request):
        language = request.META['HTTP_ACCEPT_LANGUAGE']
        result = None
        print(language)

        if language.find("en") != -1:
            result = SystemConfiguration.objects.all().first().aboutUs_en
        elif language.find("es") != -1:
            result = SystemConfiguration.objects.all().first().aboutUs_es

        return Response(result)


def isPositivefloat(string):
    try:
        float(string)
        if '-' not in string:
            return True
        else:
            return False
    except ValueError:
        return False


def isPositiveInteger(string):
    try:
        int(string)
        if '-' not in string:
            return True
        else:
            return False
    except ValueError:
        return False


def get_artist_or_customer_by_user(user):

    if user:
        artist = Artist.objects.filter(user_id=user.id).first()

        if artist is not None:
            return artist
        else:
            customer = Customer.objects.filter(user_id=user.id).first()

            if customer is not None:
                return customer

    return None

