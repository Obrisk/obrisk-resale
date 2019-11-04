from django.contrib.sitemaps import Sitemap
from .models import Question

class QASitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8
    
    def items(self):
        return Question.objects.all()
    
    def lastmod(self, obj):
        return obj.timestamp