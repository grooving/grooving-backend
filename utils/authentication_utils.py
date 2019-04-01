from Grooving.models import Artist, Customer

from rest_framework.authtoken.models import Token


def get_logged_user(request):
    try:
        token = request._auth.key
        if token is not None:
            token_object = Token.objects.all().filter(pk=token).first()
            if token_object is not None:
                user_id = token_object.user_id
                artist = Artist.objects.filter(user_id=user_id).first()
                if artist is not None:
                    return artist
                else:
                    customer = Customer.objects.filter(user_id=user_id).first()
                    if customer is not None:
                        return customer

                    else:
                        return None
        else:
            return None
    except:
        return None


def is_user_authenticated(user, request):
    return get_logged_user(request) == user


def get_artist(request):
    try:
        token = request._auth.key
        if token is not None:
            token_object = Token.objects.all().filter(pk=token).first()
            if token_object is not None:
                user_id = token_object.user_id
                artist = Artist.objects.filter(user_id=user_id).first()
                if artist is not None:
                    return artist
                else:
                    return None
        else:
            return None
    except:
        return None


def get_customer(request):
    try:
        token = request._auth.key
        if token is not None:
            token_object = Token.objects.all().filter(pk=token).first()
            if token_object is not None:
                user_id = token_object.user_id
                customer = Customer.objects.filter(user_id=user_id).first()
                if customer is not None:
                    return customer
                else:
                    return None
        else:
            return None
    except:
        return None

# Deprecated functions


def get_user_type(user):
    print("utils.authentication_utils.get_user_type is deprecated.")
    if user:
        artist = Artist.objects.filter(user_id=user.user_id).first()
        if artist is not None:
            return "Artist"
        else:
            customer = Customer.objects.filter(user_id=user.user_id).first()
            if customer is not None:
                return "Customer"
    else:
        return None
