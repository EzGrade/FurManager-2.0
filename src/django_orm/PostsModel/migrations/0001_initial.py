# Generated by Django 5.0.1 on 2024-01-09 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PostsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.TextField()),
                ('caption', models.CharField(max_length=150)),
                ('author', models.CharField(max_length=150)),
                ('tags', models.CharField(max_length=150)),
                ('test', models.CharField(max_length=150)),
            ],
        ),
    ]
