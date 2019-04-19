from django.conf.urls import url

from . import consumers

from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^chat/(?P<offer_id>[0-9]+)/$', consumers.ChatConsumer),
]
