# websocket/funcs/routing.py - DEBUG VERSION
from django.urls import re_path, path
from .consumers import PropertyConsumer
import re

# Debug: Test your regex pattern
test_path = "ws/property/ea5573a6-d447-4e65-ae54-05e6a714bd11/"
patterns = [
    r'^ws/property/(?P<property_id>[a-f0-9\-]+)/$',  # UUID specific
    r'^ws/property/(?P<property_id>[\w\-]+)/$',      # Alphanumeric + hyphens
    r'^ws/property/(?P<property_id>.+)/$',           # Any characters
]

for i, pattern in enumerate(patterns):
    match = re.match(pattern, test_path)
    

websocket_urlpatterns = [
    # Try the most permissive first for debugging
    re_path(r'^ws/property/(?P<property_id>.+)/$', PropertyConsumer.as_asgi()),
    
    # Alternative using Django's path() function
    # path('ws/property/<str:property_id>/', PropertyConsumer.as_asgi()),
]