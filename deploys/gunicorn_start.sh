#!/bin/bash

NAME="obrisk"
DIR=/home/ubuntu/obdev2018
USER=ubuntu
GROUP=ubuntu
WORKERS=3
BIND=unix:/home/ubuntu/run/gunicorn.sock
DJANGO_SETTINGS_MODULE=config.settings.production
DJANGO_WSGI_MODULE=config.wsgi
LOG_LEVEL=error

cd $DIR
source ../venv_obrisk/bin/activate

export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DIR:$PYTHONPATH

exec ../venv_obrisk/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $WORKERS \
  --user=$USER \
  --group=$GROUP \
  --bind=$BIND \
  --log-level=$LOG_LEVEL \
  --log-file=-
