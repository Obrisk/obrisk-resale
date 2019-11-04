from django.contrib.sitemaps import Sitemap
from .models import Post

class PostsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8
    
    def items(self):
        return Post.objects.all()
    
    def lastmod(self, obj):
        return obj.timestamp