from Grooving.models import Artist, Customer

from rest_framework.authtoken.models import Token


def get_logged_user(request):
    token = request._auth.key
    if token is not None:
        token_object = Token.objects.all().filter(pk=token).first()
        if token_object is not None:
            user_id = token_object.user_id
            artist = Artist.objects.filter(user_id=user_id).first()
            if artist:
                return artist
            else:
                customer = Customer.objects.filter(user_id=user_id).first()
                if customer:
                    return customer

                else:
                    return None
    else:
        return None


def is_user_authenticated(user, request):
    return get_logged_user(request) == user


def get_user_type(user):
    if user:
        artist = Artist.objects.filter(user_id=user.id).first()
        if artist:
            return "Artist"
        else:
            customer = Customer.objects.filter(user_id=user.id).first()
            if customer:
                return "Customer"
    else:
        return "None"
