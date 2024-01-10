from django.contrib.postgres.fields import ArrayField
from django.db import models

from UserModel.models import UserModel


# Create your models here.
class ChannelModel(models.Model):
    channel_id = models.CharField()
    channel_name = models.CharField(max_length=50, blank=False, null=False)
    channel_admins = ArrayField(models.BigIntegerField(), blank=True, null=True, default=list)
    channel_holder = models.ForeignKey(UserModel, on_delete=models.CASCADE, db_index=True)
    request_link = models.CharField(max_length=100, blank=True, null=True)
