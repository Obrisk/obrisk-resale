Obrisk
========

A location-based social network for foreigners in China.

.. image:: https://travis-ci.com/elshaddae/obdev2018.svg?branch=master
    :target: https://travis-ci.com/elshaddae/obdev2018
    :alt: TravisCI Status

.. image:: https://coveralls.io/github/elshaddae/obdev2018/badge.svg?branch=master
    :target: https://coveralls.io/github/elshaddae/obdev2018?branch=master
    :alt: Coverage

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
    :target: https://github.com/pydanny/cookiecutter-django/
    :alt: Built with Cookiecutter Django


A **location based** social network

The project has 5 apps:

Articles/blogging (A blogging app)
Stories (A news-feed like app)
Classifieds (Second-handed selling)
Messeger (A basic chat for communication.)
Question & Answers (A Stack Overflow-like platform)



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
