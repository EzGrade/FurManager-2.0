import django.conf

import sys
import os

sys.path.append(os.path.abspath('django_orm'))

django.conf.settings.configure(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "furmanager",
            "USER": "postgres",
            "PASSWORD": "GradeTop1!",
            "HOST": "localhost",
            "PORT": "5432",
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