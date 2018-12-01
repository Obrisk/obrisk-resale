from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class StoriesConfig(AppConfig):
    name = 'obrisk.stories'
    verbose_name = _("Stories")
