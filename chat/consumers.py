from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
from Grooving.models import Offer, Artist, Customer, Chat
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
            if self.offer.status != "CONTRACT_MADE":
                self.accept()
                self.send(text_data=json.dumps({"json":
                    {
                        'mode': 'ERROR',
                        'error': 'OFFER_NOT_IN_CONTRACT_MADE'
                    }
                }))
                self.close()

            else:
                self.customer = self.offer.eventLocation.customer
                self.artist = self.offer.paymentPackage.portfolio.artist
                self.chat = Chat.objects.filter(offer=self.offer).first()
                if self.chat is None:
                    chat = Chat(json={"init": False, "messages": None})
                    chat.save()
                    self.offer.chat=chat
                    self.offer.save()
                    self.chat = chat
                if self.chat is not None and self.chat.json is None:
                    self.chat.json = {"init": False, "messages": None}
                    self.chat.save()
                self.room_group_name = 'chat_%s' % self.room_name
                self.is_connect_to_group=False
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
        user = is_correct_user_authenticate(token, self.customer, self.artist)
        if not user[0]:
            self.send(text_data=json.dumps({"json":
                {
                    'mode': 'ERROR',
                    'error': 'PERMISSION_DENNIED_NOT_OWNER'
                }
            }))
            try:
                async_to_sync(self.channel_layer.group_discard)(
                    self.room_group_name,
                    self.channel_name
                )
            except:
                pass

            self.close()
        else:
            # Join room group
            if not self.is_connect_to_group:
                async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
                )
                self.is_connect_to_group = True

            if message is not None:
                message =  {"mode": "MESSAGE",
                       "name": str(user[1].user.first_name),
                       "username": str(user[1].user.username),
                       #"photo": str(user[1].photo),
                       "hour": get_string_time(),
                       "date": get_string_date(),
                       "message": message
                       }
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

        if not self.chat.json.get("init") or self.chat.json.get("messages") is None:
            self.chat.json["messages"] = [{"json": message}, ]
            self.chat.json["init"] = True

        else:
            dict= {"json": message}
            self.chat.json["messages"].append(dict)
            # Send message to WebSocket
        self.chat.save()
        self.send(text_data=json.dumps({
            "json": message
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


def get_string_date():
    day = str(datetime.now().day)
    if len(day) == 1:
        day = "0" + day
    month = str(datetime.now().month)
    if len(month) == 1:
        month = "0" + month
    year = str(datetime.now().year)
    return year + "-" + month +  "-" + day
def get_string_time():
    hour = str(datetime.now().hour)
    if len(hour)==1:
        hour = "0"+hour
    minute = str(datetime.now().minute)
    if len(minute)==1:
        minute = "0"+minute
    return hour + ":" + minute
#def is_correct_user_authenticate(offer, token):
