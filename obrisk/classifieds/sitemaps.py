from django.contrib.sitemaps import Sitemap
from .models import Classified


class ClassifiedsSitemap(Sitemap):
    changefreq = 'hourly'
    priority = 0.9

    def items(self):
        return Classified.objects.get_active()

    def lastmod(self, obj):
        return obj.timestamp
