from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from Grooving.models import Offer, Artist, Customer
from django.conf import settings
from channels.exceptions import DenyConnection, AcceptConnection
from utils.utils import isPositiveInteger
from datetime import datetime
from rest_framework.authtoken.models import Token


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        url = self.scope['url_route']
        self.room_name = url.get('kwargs').get('offer_id')
        if not host_is_allow(url):
            self.accept()
            self.send(text_data=json.dumps({"json":
                {

                'mode': 'ERROR',
                'error': 'NOT_ALLOWED_REQUEST_HOST'
                }
            }))
            self.close()
        elif not isPositiveInteger(self.room_name) or Offer.objects.filter(isHidden=False, pk=int(self.room_name)).first() is None:
            self.accept()
            self.send(text_data=json.dumps({"json":
                {
                'mode': 'ERROR',
                'error': 'OFFER_NOT_FOUND'
                }
            }))
            self.close()
        else:
            self.offer = Offer.objects.filter(isHidden=False, pk=int(self.room_name)).first()
            self.customer = self.offer.eventLocation.customer
            self.artist = self.offer.paymentPackage.portfolio.artist
            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name,
                self.channel_name
            )

            self.accept()

    def disconnect(self, close_code):
        # Leave room group
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
        except:
            pass

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        token = text_data_json.get("token")
        token_object = Token.objects.all().filter(pk=token).first()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'token': token
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        token = event['token']
        user = is_correct_user_authenticate(token, self.customer, self.artist)
        if not user[0]:
            self.send(text_data=json.dumps({"json":
                {
                    'mode': 'ERROR',
                    'error': 'PERMISSION_DENNIED_NOT_OWNER'
                }
            }))
            self.close()
        else:
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                "json": {"mode": "MESSAGE",
                   "name": str(user[1].user.first_name),
                   "username": str(user[1].user.username),
                   "hour": str(datetime.now().hour) +":"+ str(datetime.now().minute),
                   "message": message
                   }
            }))


def host_is_allow(host):
    alloweds = settings.ALLOWED_HOSTS
    is_allowed = False
    for allowed in alloweds:
        if allowed in host or allowed == '*':
            is_allowed = True
    if len(alloweds) == 0:
        is_allowed = True

    return is_allowed


def is_correct_user_authenticate(token, customer, artist):
    token_object = Token.objects.all().filter(pk=token).first()
    correct = False
    user = None
    if token_object is not None:
        if customer is not None and artist is not None:
            if customer.user_id == token_object.user_id:
                correct = True
                user = customer
            if artist.user_id == token_object.user_id:
                correct = True
                user = artist
    return correct, user





#def is_correct_user_authenticate(offer, token):
