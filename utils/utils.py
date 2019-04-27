from django.utils import timezone
from Grooving.models import SystemConfiguration
from rest_framework import generics
from rest_framework.response import Response
from utils.Assertions import Assertions
from Grooving.models import Artist, Customer, User


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
            if o.status == 'PENDING' and o.paymentPackage.portfolio.isHidden:
                o.status = 'REJECTED'
                #TODO: Give internationalized reason about why the offer is cancelled
                o.save()
            elif o.status == 'CONTRACT_MADE' and o.paymentPackage.portfolio.isHidden:
                o.status = 'CANCELLED_ARTIST'
                o.save()
            elif o.status == 'PENDING' and o.eventLocation.isHidden:
                o.status = 'WITHDRAWN'
                o.save()
            elif o.status == 'CONTRACT_MADE' and o.eventLocation.isHidden:
                o.status = 'CANCELLED_CUSTOMER'
                o.save()


class TermsAndConditions(generics.GenericAPIView):

    @staticmethod
    def get(request):
        language = check_accept_language(request)

        result = None

        if language == "en":
            result = SystemConfiguration.objects.all().first().termsText_en
        elif language == "es":
            result = SystemConfiguration.objects.all().first().termsText_es

        return Response(result)


class Privacy(generics.GenericAPIView):

    @staticmethod
    def get(request):
        language = check_accept_language(request)

        result = None

        if language == "en":
            result = SystemConfiguration.objects.all().first().privacyText_en
        elif language == "es":
            result = SystemConfiguration.objects.all().first().privacyText_es

        return Response(result)


class AboutUs(generics.GenericAPIView):

    @staticmethod
    def get(request):
        language = check_accept_language(request)

        result = None

        if language == "en":
            result = SystemConfiguration.objects.all().first().aboutUs_en
        elif language == "es":
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


def check_accept_language(request):
    language = ""

    try:
        request_language = request.META['HTTP_ACCEPT_LANGUAGE']

        if request_language.find("en") != -1:
            language = "en"
        elif request_language.find("es") != -1:
            language = "es"
        else:
            raise ValueError("This language is not supported")
    except ValueError as e:
        Assertions.assert_true_raise403(False, {"error": e.args[0]})
    except:
        Assertions.assert_true_raise403(False, {"error": "Language not found"})

    return language

'''
def check_accept_language_by_user(logged_user):
    language = ""

    try:
        request_language = logged_user.language
        
        if logged_user is None:
            
            language = "en"
        
        if request_language.find("en") != -1:
            language = "en"
        elif request_language.find("es") != -1:
            language = "es"
        else:
            raise ValueError("This language is not supported")
    except ValueError as e:
        Assertions.assert_true_raise403(False, {"error": e.args[0]})    
    except:
        Assertions.assert_true_raise403(False, {"error": "Language not found"})

    return language
'''