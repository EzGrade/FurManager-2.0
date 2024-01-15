import os

import django
from django.conf import settings

from .forms import *

if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_orm.django_orm.settings')
    settings.configure(
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