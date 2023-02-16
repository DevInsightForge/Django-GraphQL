"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from luna_ws import add_ws_app

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django_app = get_asgi_application()

application = add_ws_app(get_asgi_application())
