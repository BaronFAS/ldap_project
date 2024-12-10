# import os
# import django

from django.conf import settings

from auth_service.settings import *


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
# os.environ.setdefault('PYTHONPATH', '/home/fel/project/AuthService/auth-service/auth_service/')
# django.setup()


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

CACHES["default"] = {
    "BACKEND": "django.core.cache.backends.dummy.DummyCache",
}
CACHES["dummy_cache"] = {
    "BACKEND": "django.core.cache.backends.dummy.DummyCache",
}
WAFFLE_CACHE_NAME = "dummy_cache"
