# Generated by Django 5.0.1 on 2024-01-18 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChannelModel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='channelmodel',
            name='posts_number',
            field=models.IntegerField(default=1),
        ),
    ]
