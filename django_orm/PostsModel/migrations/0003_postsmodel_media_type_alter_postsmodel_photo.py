# Generated by Django 5.0.1 on 2024-01-20 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PostsModel', '0002_alter_postsmodel_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='postsmodel',
            name='media_type',
            field=models.CharField(choices=[('PHOTO', 'Photo'), ('GIF', 'Gif')], default='PHOTO', max_length=5),
        ),
        migrations.AlterField(
            model_name='postsmodel',
            name='photo',
            field=models.TextField(blank=True, null=True),
        ),
    ]
