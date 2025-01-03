"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import cam_tracker.routing
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": OriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    cam_tracker.routing.websocket_urlpatterns
                )
            ),
            ["*"]
        ) 
        
    }
)
