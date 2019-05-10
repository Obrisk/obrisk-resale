obrisk
========

A location based social network

.. image:: https://coveralls.io/repos/github/elshaddae/obrisk/badge.svg?branch=master
    :target: https://coveralls.io/github/elshaddae/obrisk?branch=master
    :alt: Coverage

.. image:: https://requires.io/github/vitorfs/elshaddae/requirements.svg?branch=master
    :target: https://requires.io/github/vitorfs/elshaddae/requirements/?branch=master
    :alt: Requirements

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
    :target: https://github.com/pydanny/cookiecutter-django/
    :alt: Built with Cookiecutter Django

The project has 5 apps:

* Post (A blogging app)
* Stories (A Twitter-like microblog)
* Classifieds (Second-handed selling)
* Question & Answers (A Stack Overflow-like platform)
* Messeger (A basic chat for communication.)

Technology Stack
----------------
.. _Python: https://www.python.org/
.. _`Django Web Framework`: https://www.djangoproject.com/
.. _PostgreSQL: https://www.postgresql.org/
.. _`Redis 4.2`: https://redis.io/documentation
.. _Uvicorn: https://github.com/encode/uvicorn/
.. _Docker: https://docs.docker.com/
.. _docker-compose: https://docs.docker.com/compose/
.. _WhiteNoise: http://whitenoise.evans.io/en/stable/
.. _`Twitter Bootstrap 4`: https://getbootstrap.com/docs/4.0/getting-started/introduction/
.. _`jQuery 3`: https://api.jquery.com/
.. _Django-channels: https://channels.readthedocs.io/en/latest/
.. _Sentry: https://docs.sentry.io/
.. _Mailgun: https://www.mailgun.com/
.. _Cookiecutter: http://cookiecutter-django.readthedocs.io/en/latest/index.html

Basic Commands
--------------

Test coverage
^^^^^^^^^^^^^
To run the tests, check your test coverage, and generate a simplified coverage report::

    $ pytest

To generate an HTML report::

    $ coverage html
    $ open htmlcov/index.html

To check the report in console::

    $ coverage report -m

Sentry
^^^^^^

Sentry is an error logging aggregator service. You can host it by yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

.. _`sign up`: https://sentry.io/signup/?code=cookiecutter

You must set the DSN url in production.


Deployment
----------

With Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
