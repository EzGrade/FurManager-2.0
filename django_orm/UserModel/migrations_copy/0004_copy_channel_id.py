# Generated by Django 5.0.1 on 2024-01-10 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserModel', '0003_alter_usermodel_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='channel_id',
        ),
    ]