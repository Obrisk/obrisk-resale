from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FriendConfig(AppConfig):
    name = 'obrisk.friend'
    verbose_name = _('Friend')
