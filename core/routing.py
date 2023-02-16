from django.urls import path
from core.consumers import GraphQLWebSocketHandler

ws_urlpatterns = [path("ws/", GraphQLWebSocketHandler.as_asgi())]
