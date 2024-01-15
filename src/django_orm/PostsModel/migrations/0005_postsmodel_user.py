# Generated by Django 5.0.1 on 2024-01-09 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PostsModel', '0004_remove_postsmodel_test'),
        ('UserModel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postsmodel',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='UserModel.usermodel'),
        ),
    ]