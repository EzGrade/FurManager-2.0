# Generated by Django 5.0.1 on 2024-01-10 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserModel', '0005_usermodel_channel_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='request_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]