import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

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
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'PostsModel.apps.PostsmodelConfig',
        'UserModel.apps.UsermodelConfig',
        'ChannelModel.apps.ChannelmodelConfig',
    ]
)

django.setup()