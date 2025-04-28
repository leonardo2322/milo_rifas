import os
import django
from environ import Env

env = Env()
# Lee el archivo .env si existe
env.read_env()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', env.str('DJANGO_SETTINGS_MODULE', default='milo_rifas.settings'))


# 👇 Aquí, muy importante, antes de cualquier modelo:
django.setup()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from gestor_rifa import routing
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(routing.websocket_urlpatterns)
    ),
})
