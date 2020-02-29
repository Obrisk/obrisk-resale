from __future__ import absolute_import, unicode_literals
import os, environ, sys
from celery import Celery
from config.settings.base import ROOT_DIR

env = environ.Env()
env.read_env(str(ROOT_DIR.path('.env')))

# This allows easy placement of apps within the interior
# obrisk directory.
app_path = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.append(os.path.join(app_path, 'obrisk'))

# set the default Django settings module for the 'celery' program.
os.environ.setdefault(env('DJANGO_SETTINGS_MODULE'),
                      'config.settings.production')

app = Celery('obrisk')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
