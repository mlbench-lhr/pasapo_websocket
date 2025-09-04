from django.urls import re_path, path
from .consumers import PropertyConsumer, GuestConsumer
import re

# Debug: Test your regex patterns
test_paths = [
    "ws/property/ea5573a6-d447-4e65-ae54-05e6a714bd11/",
    "ws/guest/guest_123_abc/"
]

patterns = [
    r'^ws/property/(?P<property_id>[a-f0-9\-]+)/$',  # UUID specific
    r'^ws/property/(?P<property_id>[\w\-]+)/$',      # Alphanumeric + hyphens
    r'^ws/property/(?P<property_id>.+)/$',           # Any characters
    r'^ws/guest/(?P<guest_id>[a-f0-9\-]+)/$',       # UUID specific for guests
    r'^ws/guest/(?P<guest_id>[\w\-]+)/$',            # Alphanumeric + hyphens for guests
    r'^ws/guest/(?P<guest_id>.+)/$',                 # Any characters for guests
]

for test_path in test_paths:
    print(f"Testing path: {test_path}")
    for i, pattern in enumerate(patterns):
        match = re.match(pattern, test_path)
        if match:
            print(f"  ✅ Pattern {i}: {pattern} -> {match.groupdict()}")
        else:
            print(f"  ❌ Pattern {i}: {pattern}")
    print()

websocket_urlpatterns = [
    # Try the most permissive first for debugging
    re_path(r'^ws/property/(?P<property_id>.+)/$', PropertyConsumer.as_asgi()),
    re_path(r'^ws/guest/(?P<guest_id>.+)/$', GuestConsumer.as_asgi()),
]