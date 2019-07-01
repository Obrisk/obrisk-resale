obrisk
========

An enterprise oriented social network

.. image:: https://travis-ci.org/vitorfs/obrisk.svg?branch=master
    :target: https://travis-ci.org/vitorfs/obrisk
    :alt: TravisCI Status

.. image:: https://coveralls.io/repos/github/vitorfs/obrisk/badge.svg?branch=master
    :target: https://coveralls.io/github/vitorfs/obrisk?branch=master
    :alt: Coverage

.. image:: https://requires.io/github/vitorfs/obrisk/requirements.svg?branch=master
    :target: https://requires.io/github/vitorfs/obrisk/requirements/?branch=master
    :alt: Requirements

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
    :target: https://github.com/pydanny/cookiecutter-django/
    :alt: Built with Cookiecutter Django

:License: MIT

A **location based** social network

The project has 5 apps:

Post (A blogging app)
Stories (A Twitter-like microblog)
Classifieds (Second-handed selling)
Question & Answers (A Stack Overflow-like platform)
Messeger (A basic chat for communication.)


Basic Instructions
--------------

For the chat app to work please create a superuser as the url will need the kwarg of admin username.
For development when running manage.py file please pass a flag --settings=config.settings.local to reflect the local changes.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate a simplified coverage report::

    $ pytest

To generate an HTML report::

    $ coverage html
    $ open htmlcov/index.html

To check the report in console::

    $ coverage report -m



Deployment
----------

The following details how to deploy this application.


Heroku
^^^^^^

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html


Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
