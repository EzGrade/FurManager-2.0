#!/bin/sh

python3 app.py &
python3 django_orm/manage.py runserver 0.0.0.0:8000