"""
Base settings to build other settings files upon.
"""
import environ, os

ROOT_DIR = environ.Path(__file__) - 3  # (obrisk/config/settings/base.py - 3 = obrisk/)
APPS_DIR = ROOT_DIR.path('obrisk')

env = environ.Env()
env.read_env(str(ROOT_DIR.path('.env')))

# READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
# if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    # env.read_env(str(ROOT_DIR.path('.env')))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

#INTERNATIONALIZATION 
# ------------------------------------------------------------------------------
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = 'Asia/Chongqing'
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('sw', 'Swahili'),
)

LOCALE_PATHS = [
    str(ROOT_DIR.path('locale')),
]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db('DATABASE_URL'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'config.urls'
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'dal',   #Django auto complete has to be before admin
    'dal_select2',
    'django.contrib.admin',
    'django.forms',
]
THIRD_PARTY_APPS = [
    'crispy_forms',
    'sorl.thumbnail',
    'phonenumber_field',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 'allauth.socialaccount.providers.amazon',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.linkedin',
    # 'allauth.socialaccount.providers.slack',
    'channels',
    'graphene_django',
    'markdownx',
    'taggit',
    'star_ratings',
    'friendship',
    'pwa_webpush',
    
]
LOCAL_APPS = [
    'obrisk.users.apps.UsersConfig',
    # Your stuff: custom apps go here
    'obrisk.friend.apps.FriendConfig',        
    'obrisk.classifieds.apps.ClassifiedsConfig',
    'obrisk.messager.apps.MessagerConfig',
    'obrisk.stories.apps.StoriesConfig',
    'obrisk.notifications.apps.NotificationsConfig',
    'obrisk.qa.apps.QaConfig',
    'obrisk.search.apps.SearchConfig',
    'obrisk.posts.apps.PostsConfig',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

FORM_RENDERER = 'django.forms.renderers.TemplatesSetting' 

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {
    'sites': 'obrisk.contrib.sites.migrations'
}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'users.phone_authentication.PhoneAuthBackend',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'users.User'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = 'classifieds:list'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = 'account_login'

SESSION_COOKIE_AGE = 60 * 60 * 24 * 40 #40 Days.

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# STATIC
# -------------------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'obrisk.classifieds.context_processors.cached_queries',
            ],
        },
    },
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env('ADMIN_URL', default='admin/')

# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
     ('Elisha Kingdom', 'el@obrisk.com'),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# django-allauth
# ------------------------------------------------------------------------------
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ALLOW_REGISTRATION = env.bool('ACCOUNT_ALLOW_REGISTRATION', True)

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'

#This is because of overiding login forms on users.forms
#options are False and True for the remember me box
SESSION_REMEMBER = None

ACCOUNT_EMAIL_VERIFICATION = 'optional'

SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'

#This will avoid the duplicates in usernames with diff casing
ACCOUNT_PRESERVE_USERNAME_CASING = True

USERNAME_MIN_LENGTH = 3

ACCOUNT_FORMS = {
    'signup': 'users.forms.PhoneSignupForm', 
    'login': 'users.forms.CustomLoginForm'
}

ACCOUNT_USERNAME_BLACKLIST = ['AnonymousUser', 'admin', 'obrisk']

ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

SOCIALACCOUNT_ADAPTER = 'obrisk.users.adapters.SocialAccountAdapter'
#ACCOUNT_ADAPTER = 'obrisk.users.adapters.AccountAdapter'


# SOCIALACCOUNT_PROVIDERS = {
#     'weixin': {
#         'AUTHORIZE_URL': 'https://open.weixin.qq.com/connect/oauth2/authorize',  # for media platform
#         'SCOPE': ['snsapi_base'],
#     }
# }


# Other stuff...
# ------------------------------------------------------------------------------

# REDIS setup
REDIS_URL = f'{env("REDIS_URL", default="redis://127.0.0.1:6379")}/{0}'

# django-channels setup
ASGI_APPLICATION = 'config.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL, ],
        },
    }
}

# GraphQL settings
GRAPHENE = {
    'SCHEMA': 'obrisk.schema.schema'
}

#Max data to be uploaded to Django server. This is around 12MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 13000000

FILE_UPLOAD_MAX_MEMORY_SIZE = 13000000

TAGS_CACHE_TIMEOUT = 60 * 60 * 24 * 7 #7 days. 

PWA_APP_NAME = 'Obrisk'
PWA_APP_DESCRIPTION = 'A location based social network for foreigners in China'
PWA_APP_THEME_COLOR = '#3ec4e2'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = "/"
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = "/"
PWA_APP_ICONS = [    {
        "src": "/static/img/android-chrome-192x192.png",
        "sizes": "192x192",
    }, {
        "src": "/static/img/android-chrome-512x512.png",
        "sizes": "512x512",
    }
    , {
        "src": "/static/img/mstile-310x310.png",
        "sizes": "310x310",
    }, {
        "src": "/static/img/mstile-310x150.png",
        "sizes": "310x150",
    }, {
        "src": "/static/img/mstile-150x150.png",
        "sizes": "150x150",
    }, {
        "src": "/static/img/mstile-144x144.png",
        "sizes": "144x144",
    }
    , {
        "src": "/static/img/mstile-70x70.png",
        "sizes": "70x70",
    }]
 

PWA_APP_SPLASH_SCREEN = [
    {
        'src': 'static/img/android-chrome-192x192.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = '/'
PWA_APP_LANG = 'en-US'
PWA_SERVICE_WORKER_PATH = APPS_DIR.path('templates/serviceworker.js')
