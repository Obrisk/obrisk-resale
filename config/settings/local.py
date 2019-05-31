import logging

from django.utils.log import DEFAULT_LOGGING

from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DEBUG', default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env('SECRET_KEY', default='fOqtAorZrVqWYbuMPOcZnTzw2D5bKeHGpXUwCaNBnvFUmO1njCQZGz05x1BhDG0E')
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    #"localhost",
    #"0.0.0.0",
	#"127.0.0.1",
     '*'
]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
      'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # noqa F405

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = 'localhost'
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025


# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration  # noqa F405
# https://github.com/aliyun/django-oss-storage
INSTALLED_APPS += ['django_oss_storage', 'django_extensions']  # noqa F405


#For running collectstatic local and reduce noise to the server!

#I serve them in oss bucket when scaling up, don't duplicate static files in every server.
# ------------------------
STATICFILES_STORAGE = 'django_oss_storage.backends.OssStaticStorage'

# AliCloud access key ID
OSS_ACCESS_KEY_ID = env('OSS_STS_ID')

# AliCloud access key secret
OSS_ACCESS_KEY_SECRET = env('OSS_STS_KEY')

# The name of the bucket to store files in
OSS_BUCKET_NAME = env('OSS_BUCKET')

# The URL of AliCloud OSS endpoint
# Refer https://www.alibabacloud.com/help/zh/doc-detail/31837.htm for OSS Region & Endpoint
OSS_ENDPOINT = env('OSS_ENDPOINT')

OSS_COVERAGE_IF_FILE_EXIST = True

OSS_FILE_SAVE_AS_URL = False

# The expire time to construct signed url for private acl bucket.
# Can be set by OSS_EXPIRE_TIME as environment variable or as Django settings.
#The default value is 30 days. I took the values from AWS_EXPIRY in sample project
OSS_EXPIRE_TIME =  60 * 60 * 24 * 7

# The default location for the static files stored in bucket.
OSS_STATIC_LOCATION = '/static/'

# The default location for your static files
STATIC_ROOT =  '/static/'

STATIC_URL =  '/static/'

#django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ['debug_toolbar']  # noqa F405

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ['127.0.0.1', '10.0.2.2']
import socket
import os
if os.environ.get('USE_DOCKER') == 'yes':
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1' for ip in ips]

# Your stuff...



