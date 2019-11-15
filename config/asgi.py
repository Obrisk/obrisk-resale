"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os, sys
import django
from channels.routing import get_default_application

# This allows easy placement of apps within the interior
# obrisk directory.
app_path = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.append(os.path.join(app_path, 'obrisk'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
django.setup()
application = get_default_application()
