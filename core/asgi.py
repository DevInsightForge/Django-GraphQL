"""
ASGI config for core project.

"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path

from core.consumers import MyGraphqlWsConsumer
from core.middlewares import WsMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

http_application = get_asgi_application()

ws_application = WsMiddlewareStack(
    URLRouter(
        [
            path("graphql/", MyGraphqlWsConsumer.as_asgi()),
        ]
    )
)

application = ProtocolTypeRouter(
    {
        "http": http_application,
        "websocket": ws_application,
    }
)
