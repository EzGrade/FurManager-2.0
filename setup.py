import os

import django

os.path.abspath("django_orm")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_orm.django_orm.settings')

django.setup()
