from django.conf.urls import url

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from obrisk.messager.consumers import MessagerConsumer
from obrisk.notifications.consumers import NotificationsConsumer
# from obrisk.notifications.routing import notifications_urlpatterns
# from obrisk.messager.routing import messager_urlpatterns

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                url(r'^ws/notifications/$', NotificationsConsumer),
                url(r'^ws/messages/(?P<username>([^/]+))/$', MessagerConsumer),
            ])
        ),
    ),
})