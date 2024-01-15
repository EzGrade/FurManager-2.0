# import os
#
# import django
# from django.conf import settings
#
# if not settings.configured:
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_orm.django_orm.settings')
#     settings.configure(
#         DATABASES={
#             "default": {
#                 "ENGINE": "django.db.backends.postgresql",
#                 "NAME": "furmanager",
#                 "USER": "postgres",
#                 "PASSWORD": "GradeTop1!",
#                 "HOST": "localhost",
#                 "PORT": "5432",
#             }
#         },
#         INSTALLED_APPS=[
#             'rest_framework',
#             'django_orm.django_orm',
#             'django_orm.PostsModel'
#         ]
#     )
#     django.setup()
