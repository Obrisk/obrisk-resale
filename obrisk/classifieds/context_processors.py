from django.core.cache import cache
from obrisk.classifieds.models import Classified

def cached_queries(request):
    popular_tags = cache.get('popular_tags')

    if popular_tags == None:
        popular_tags = Classified.objects.get_counted_tags()

    return {'popular_tags': popular_tags}