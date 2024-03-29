import os
import sys, environ
from config.settings.base import ROOT_DIR

env = environ.Env()
env.read_env(str(ROOT_DIR.path('.env')))
#
#os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.production'

if __name__ == '__main__':
    os.environ.setdefault(env('DJANGO_SETTINGS_MODULE'), 'config.settings.production')

    try:
        from django.core.management import execute_from_command_line

    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions.
        try:
            import django  # noqa

        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    # This allows easy placement of apps within the inner obrisk directory.
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(current_path, 'obrisk'))

    execute_from_command_line(sys.argv)
