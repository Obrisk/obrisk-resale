#!/bin/bash

systemctl restart gunicorn.service uvicorn.service celery.service celerybeat.service
