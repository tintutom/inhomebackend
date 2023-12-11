import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from chat.routing import websocket_urlpatterns
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inhome_doctor_consulting.settings')


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        'websocket': URLRouter(websocket_urlpatterns),

    }
)
