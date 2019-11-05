#!/bin/bash

source venv_obrisk/bin/activate
pip install -r requirements/production.txt
python /home/obdev-user/obdev2018/manage.py migrate
python /home/obdev-user/obdev2018/manage.py collectstatic --settings=config.settings.static #Pass the settings parameter only when django-storages is not working