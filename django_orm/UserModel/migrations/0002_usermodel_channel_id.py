# Generated by Django 5.0.1 on 2024-01-09 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserModel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='channel_id',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
    ]
