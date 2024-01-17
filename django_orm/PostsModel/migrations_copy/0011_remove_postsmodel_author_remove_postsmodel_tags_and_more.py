# Generated by Django 5.0.1 on 2024-01-12 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChannelModel', '0005_channelmodel_channel_delay'),
        ('PostsModel', '0010_alter_postsmodel_author_alter_postsmodel_photo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postsmodel',
            name='author',
        ),
        migrations.RemoveField(
            model_name='postsmodel',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='postsmodel',
            name='user',
        ),
        migrations.AddField(
            model_name='postsmodel',
            name='caption',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='postsmodel',
            name='channels',
            field=models.ManyToManyField(blank=True, to='ChannelModel.channelmodel'),
        ),
    ]