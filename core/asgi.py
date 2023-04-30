"""
ASGI config for core project.

"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path

from core.consumers import MyGraphqlWsConsumer
from core.middlewares import WsMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": WsMiddlewareStack(
            URLRouter([path("graphql/", MyGraphqlWsConsumer.as_asgi())])
        ),
    }
)
