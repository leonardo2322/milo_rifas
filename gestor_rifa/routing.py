from django.urls import re_path

from consumers.consumer import Consumirdorwebsocket

websocket_urlpatterns = [
    re_path(r'ws/numeros/$', Consumirdorwebsocket.as_asgi()),
    re_path(r'ws/numeros/(?P<cliente_id>\d+)/$', Consumirdorwebsocket.as_asgi()),
]

