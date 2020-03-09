import logging,os
import sentry_sdk

from .base import *
from .base import env

from django.utils import timezone
from django.conf import settings
from sentry_sdk.integrations.django import DjangoIntegration

#from obrisk.utils.cloudfront import STATIC_VERSION or None
STATIC_VERSION = 'ver10032001' 

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env('SECRET_KEY')

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
#https://stackoverflow.com/questions/16676314/should-server-ip-address-be-in-allowed-hosts-django-setting
<<<<<<< HEAD
ALLOWED_HOSTS = ['www.obrisk.com', 'obrisk.com', '63.0.0.14', '63.0.0.6', '52.82.70.154', '161.189.161.69' ]
=======
#Remember to add the subdomains when applying for SSL cert and also add it in nginx file
ALLOWED_HOSTS = ['www.obrisk.com', 'obrisk.com']
>>>>>>> fixing travic basics errors

# DATABASES
# ------------------------------------------------------------------------------
DATABASES['default'] = env.db('DATABASE_URL')  # noqa F405
DATABASES['default']['ENGINE'] = 'django_db_geventpool.backends.postgresql_psycopg2'
DATABASES['default']['ATOMIC_REQUESTS'] = False  # From django-db-geventpool
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=0)  # From django-db-geventpool

# CACHES
# ------------------------------------------------------------------------------

# REDIS setup
REDIS_URL = f'{env("PRIMARY_REDIS_URL", default="redis://127.0.0.1:6379")}/{0}'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL, ],
        },
    }
}


CELERY_BROKER_URL = REDIS_URL


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            REDIS_URL,
            env('SLAVE_REDIS_URL'),
        ],
        "OPTIONS": {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            'IGNORE_EXCEPTIONS': True,
        }
    }
}




# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('SECURE_CONTENT_TYPE_NOSNIFF', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = 'DENY'

# https://github.com/aliyun/django-oss-storage

INSTALLED_APPS += ['storages','django_oss_storage']  # noqa F405


# STATIC
# ----------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
#STATIC_ROOT = str(ROOT_DIR('staticfiles'))

if os.getenv('USE_S3_STATICFILES'):
    AWS_ACCESS_KEY_ID = os.getenv('AWS_STATIC_S3_KEY_ID')

    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_STATIC_S3_S3KT')

    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    
    AWS_S3_REGION_NAME=os.getenv('AWS_S3_REGION_NAME')
    
    AWS_S3_HOST=os.getenv('AWS_S3_HOST_NAME')

    AWS_DEFAULT_ACL = 'public-read'
    
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    STATIC_URL = f'https://dist.obrisk.com/static/{STATIC_VERSION}/'
         
    if not os.getenv('CLOUDFRONT'):
        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/{STATIC_VERSION}/'

    AWS_S3_CUSTOM_DOMAIN= 'dist.obrisk.com'

    # General optimization for faster delivery
    AWS_IS_GZIPPED = True
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    #https://www.caktusgroup.com/blog/2014/11/10/Using-Amazon-S3-to-store-your-Django-sites-static-and-media-files/
    #If this import goes before secret key, raises errors
    STATICFILES_LOCATION = f'static/{STATIC_VERSION}'
    
    #The value from docs is 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'

else:
    STATICFILES_STORAGE = 'django_oss_storage.backends.OssStaticStorage'

    # AliCloud access key ID
    OSS_ACCESS_KEY_ID = env('RAM_USER_ID')

    # AliCloud access key secret
    OSS_ACCESS_KEY_SECRET = env('RAM_USER_S3KT_KEY')

    # The name of the bucket to store files in OSS_BUCKET_NAME = env('OSS_BUCKET')

    # The URL of AliCloud OSS endpoint
    # Refer https://www.alibabacloud.com/help/zh/doc-detail/31837.htm for OSS Region & Endpoint
    OSS_ENDPOINT = env('OSS_ENDPOINT')

    # The expire time to construct signed url for private acl bucket.
    # Can be set by OSS_EXPIRE_TIME as environment variable or as Django settings.
    #The default value is 30 days. I took the values from AWS_EXPIRY in sample project
    OSS_EXPIRE_TIME =  60 * 60 * 24 * 7

    # The default location for the static files stored in bucket.
    OSS_STATIC_LOCATION = '/static/'

    OSS_COVERAGE_IF_FILE_EXIST = True

    OSS_FILE_SAVE_AS_URL = False

    STATIC_URL =  '/static/'



# MEDIA
# ------------------------------------------------------------------------------
# The default location for the media files stored in bucket.

#I serve them in oss bucket when scaling up, don't duplicate static files in every server.
# ------------------------
DEFAULT_FILE_STORAGE = 'django_oss_storage.backends.OssMediaStorage'

OSS_MEDIA_LOCATION = '/media/'

MEDIA_URL = '/media/'


# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]['OPTIONS']['loaders'] = [  # noqa F405
    (
        'django.template.loaders.cached.Loader',
        [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]
    ),
]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    'DEFAULT_FROM_EMAIL',
    default='Obrisk <notifications@obrisk.com>'
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env('SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX', default='[Obrisk]')

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env('ADMIN_URL')

# Anymail (Mailgun)
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
INSTALLED_APPS += ['anymail']  # noqa F405
EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
ANYMAIL = {
    'MAILGUN_API_KEY': env('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': env('MAILGUN_SENDER_DOMAIN')
}

# raven
# ------------------------------------------------------------------------------
# https://docs.sentry.io/clients/python/integrations/django/
#INSTALLED_APPS += ['raven.contrib.django.raven_compat']  # noqa F405
#MIDDLEWARE = ['raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware'] + MIDDLEWARE

#Sentry
#------------------------------------------------------------------------------
#SENTRY_CLIENT = env('SENTRY_CLIENT', default='raven.contrib.django.raven_compat.DjangoClient')


sentry_sdk.init(
    dsn=env('SENTRY_DSN'),
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)


#SENTRY_CELERY_LOGLEVEL = env.int('SENTRY_LOG_LEVEL', logging.INFO)

#RAVEN_CONFIG = {
    #'CELERY_LOGLEVEL': env.int('SENTRY_LOG_LEVEL', logging.INFO),
#    'DSN': SENTRY_DSN
#}

# Other stuffs...
# ------------------------------------------------------------------------------

#SESSION
#Improve performance
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

PHONE_SIGNUP_DEBUG = False
