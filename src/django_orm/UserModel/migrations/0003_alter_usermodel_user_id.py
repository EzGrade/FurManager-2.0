# Generated by Django 5.0.1 on 2024-01-10 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserModel', '0002_usermodel_channel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='user_id',
            field=models.PositiveBigIntegerField(db_index=True),
        ),
    ]