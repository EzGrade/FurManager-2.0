# Generated by Django 5.0.1 on 2024-01-20 14:29

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PostsModel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postsmodel',
            name='photo',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None),
        ),
    ]