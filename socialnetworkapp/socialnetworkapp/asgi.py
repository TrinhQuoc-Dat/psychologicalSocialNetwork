"""
ASGI config for socialnetworkapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "socialnetworkapp.settings")
django.setup()

import notifications.routing
from socialnetworkapp.middlewares import OAuthTokenMiddleware


application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": OAuthTokenMiddleware(
        URLRouter(
            notifications.routing.websocket_urlpatterns
        )
    ),
})
