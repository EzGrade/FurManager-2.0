import os
import sys

import django.conf

sys.path.append(os.path.abspath('django_orm'))

if not django.conf.settings.configured:
    django.conf.settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'defaultdb',
                'USER': 'doadmin',
                'PASSWORD': 'AVNS_upLjkxOrOll61wKv5ZO',
                'HOST': 'furmanagerdb-do-user-15552012-0.c.db.ondigitalocean.com',
                'PORT': '25060',
                'OPTIONS': {
                    'sslmode': 'require',
                },
            }
        },
        INSTALLED_APPS=[
            'rest_framework',
            'PostsModel.apps.PostsmodelConfig',
            'UserModel.apps.UsermodelConfig',
            'ChannelModel.apps.ChannelmodelConfig',
        ]
    )
django.setup()
