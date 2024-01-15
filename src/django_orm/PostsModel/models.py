from django.db import models

from ChannelModel.models import ChannelModel
from UserModel.models import UserModel


# Create your models here.
class PostsModel(models.Model):
    photo = models.TextField(blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    channels = models.ManyToManyField(ChannelModel, blank=True)

    class Meta:
        app_label = 'PostsModel'

    def __str__(self):
        return f"Post #{self.pk}"
