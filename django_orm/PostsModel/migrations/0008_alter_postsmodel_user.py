# Generated by Django 5.0.1 on 2024-01-09 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PostsModel', '0007_alter_postsmodel_user'),
        ('UserModel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postsmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UserModel.usermodel'),
        ),
    ]
