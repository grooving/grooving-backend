from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from rest_framework import generics
from chat.serializer import ChatSerializer
from Grooving.models import Chat, Offer
from rest_framework import status
from rest_framework.response import Response
from utils.Assertions import Assertions
from utils.authentication_utils import get_artist, get_customer
def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })


class ListChatMesages(generics.RetrieveAPIView):

    serializer_class = ChatSerializer

    def get_queryset(self):

        return Chat.objects.all()

    def get(self, request, *args, **kwargs):
        offer = Offer.objects.filter(pk=kwargs.get("pk")).first()
        Assertions.assert_true_raise403(offer is not None, {"error": "DENIED_PEMISSION_CHAT"})

        customer = offer.eventLocation.customer
        artist = offer.paymentPackage.portfolio.artist
        Assertions.assert_true_raise403(artist is not None and customer is not None, {"error": "DENIED_PEMISSION_CHAT"})
        logedCustomer = get_customer(request)
        logedArtist = get_artist(request)
        Assertions.assert_true_raise403(logedArtist is not None or logedCustomer is not None, {"error": "DENIED_PEMISSION_CHAT"})
        if logedArtist is not None:
            Assertions.assert_true_raise403(logedArtist.id == artist.id, {"error": "DENIED_PERMISSION_CHAT_ARTIST"})
        if logedCustomer is not None:
            Assertions.assert_true_raise403(logedCustomer.id == customer.id, {"error": "DENIED_PERMISSION_CHAT_CUSTOMER"})

        chat = offer.chat
        messages = []
        if chat is None or chat.json.get("messages") is None:
            messages = []
        else:
            messages = chat.json.get("messages")

        return Response({"customerPhoto": customer.photo, "customerUsername": customer.user.username, "customerName": customer.user.first_name,
                         "artistPhoto": artist.photo, "artistUsername": artist.user.username, "artistName": artist.user.first_name,
                         "messages": messages},
                        status=status.HTTP_200_OK)