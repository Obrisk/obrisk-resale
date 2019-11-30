from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ConnectionsConfig(AppConfig):
    name = 'obrisk.connections'
    verbose_name = _('Connections')
