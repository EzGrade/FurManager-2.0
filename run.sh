#!/bin/sh

nohup python3 app.py >> output.log &
nohup python3 timer/auto_post.py >> timer/output.log &

cd django_orm

python3 manage.py runserver 0.0.0.0:8080