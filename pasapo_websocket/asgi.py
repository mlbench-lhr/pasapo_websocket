"""
ASGI config for pasapo_websocket project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

"""
ASGI config for pasapo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pasapo.settings")

# application = get_asgi_application()

# pasapo/asgi.py - DEBUG VERSION
# pasapo/asgi.py - WORKING VERSION
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pasapo_websocket.settings')

# Import Django first
django_asgi_app = get_asgi_application()

# Now import your consumers (after Django setup)
from websocket.funcs.consumers import PropertyConsumer, GuestConsumer

# Define WebSocket URL patterns
websocket_urlpatterns = [
    path('ws/property/<str:property_id>/', PropertyConsumer.as_asgi()),
    path('ws/guest/<str:guest_id>/', GuestConsumer.as_asgi()),
]

# Create the application
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})