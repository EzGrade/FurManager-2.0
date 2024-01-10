from django.contrib.postgres.fields import ArrayField
from django.db import models


# Create your models here.
class UserModel(models.Model):
    user_id = models.PositiveBigIntegerField(blank=False, null=False, db_index=True)
    user_name = models.CharField(max_length=50, blank=False, null=False, db_index=True)
    post_delay = models.IntegerField(blank=False, null=False, default=1)
    channel_id = ArrayField(models.BigIntegerField(), blank=True, null=True, default=list)
