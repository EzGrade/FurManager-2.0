# Generated by Django 5.0.1 on 2024-01-12 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChannelModel', '0010_alter_channelmodel_delay_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='channelmodel',
            name='last_post',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]