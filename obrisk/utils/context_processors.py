from django.conf import settings
from django.core.cache import cache


def cached_queries(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')

    oss = 'https://obrisk.oss-cn-hangzhou.aliyuncs.com'

    new_msgs = popular_cities = None
    if request.user.is_authenticated:
        new_msgs = cache.get(f'msg_{request.user.pk}')
    else:
        popular_cities = ['Hangzhou', 'Ningbo', 'Shanghai', 'Shaoxing']

    env = 'local'
    if not getattr(settings, 'PHONE_SIGNUP_DEBUG', False):
        env = 'prod'

    return {'new_msgs': new_msgs,
            'vapid_key': vapid_key,
            'oss': oss,
            'env': env,
            'popular_cities': popular_cities
            }
