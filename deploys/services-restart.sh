#!/bin/bash
#Nginx should be restarted manually because a lot can go wrong at least for now!

sudo systemctl restart gunicorn.service uvicorn.service celery.service celerybeat.service
