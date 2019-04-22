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

# django-debug-toolbar
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

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ['django_extensions','environ']  # noqa F405


S3DIRECT_DESTINATIONS = {
    'example_destination': {
        # "key" [required] The location to upload file
        #       1. String: folder path to upload to
        #       2. Function: generate folder path + filename using a function  
        'key': 'uploads/images',
    
        # "auth" [optional] Limit to specfic Django users
        #        Function: ACL function
        'auth': lambda u: u.is_staff,
    
        # "allowed" [optional] Limit to specific mime types
        #           List: list of mime types
        'allowed': ['image/jpeg', 'image/png', 'video/mp4'],

        # "bucket" [optional] Bucket if different from AWS_STORAGE_BUCKET_NAME
        #          String: bucket name
        'bucket': 'custom-bucket',

        # "endpoint" [optional] Endpoint if different from AWS_S3_ENDPOINT_URL
        #            String: endpoint URL
        'endpoint': 'custom-endpoint',

        # "region" [optional] Region if different from AWS_S3_REGION_NAME
        #          String: region name
        'region': 'custom-region', # Default is 'AWS_S3_REGION_NAME'
        
        # "acl" [optional] Custom ACL for object, default is 'public-read'
        #       String: ACL
        'acl': 'private',

        # "cache_control" [optional] Custom cache control header
        #                 String: header
        'cache_control': 'max-age=2592000',

        # "content_disposition" [optional] Custom content disposition header
        #                       String: header
        'content_disposition': lambda x: 'attachment; filename="{}"'.format(x),

        # "content_length_range" [optional] Limit file size
        #                        Tuple: (from, to) in bytes
        'content_length_range': (5000, 20000000),

        # "server_side_encryption" [optional] Use serverside encryption
        #                          String: encrytion standard
        'server_side_encryption': 'AES256',

        # "allow_existence_optimization" [optional] Checks to see if file already exists,
        #                                returns the URL to the object if so (no upload)
        #                                Boolean: True, False
        'allow_existence_optimization': False,
    },
    'example_destination_two': {
        'key': lambda filename, args: args + '/' + filename,
    	'key_args': 'uploads/images',
    }
}


# Your stuff...
# ------------------------------------------------------------------------------
CHAT_WS_SERVER_HOST = '192.168.0.105'
CHAT_WS_SERVER_PORT = 8001
CHAT_WS_SERVER_PROTOCOL = 'ws'
DATETIME_FORMAT ='M d H:i'


