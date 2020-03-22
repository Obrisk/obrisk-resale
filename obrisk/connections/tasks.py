from config.celery import app
from obrisk.users.models import User
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT


@app.task
def build_recommended_users():
    '''This is a background task that checks all current authenticated users and
    build a connections recommendation list for them. In the near future we have
    to handle the case of the users that were authenticated only before or after
    the task and they are excluded from this list'''
    
    
    users = User.objects.all()

    for user in users:
        if user.is_authenticated():
            #Will improve this to consider connections of connections.
            recommended_users = users.filter(city=user.city).exclude(thumbnail=None)
            
            if recommended_users.count > 20:
                TAGS_TIMEOUT = getattr(settings, 'CONNECTS_RECOMMENDATION_TIMEOUT', DEFAULT_TIMEOUT)
                cache.set(f'recommended_connects_{user.id}', recommended_users, timeout=TAGS_TIMEOUT)
            else:
                TAGS_TIMEOUT = getattr(settings, 'CONNECTS_RECOMMENDATION_TIMEOUT', DEFAULT_TIMEOUT)
                cache.set(f'recommended_connects_{user.id}', recommended_users, timeout=TAGS_TIMEOUT)
        