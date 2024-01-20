from django.db import models

from ChannelModel.models import ChannelModel
from UserModel.models import UserModel


class PostsModel(models.Model):
    MEDIA_TYPES = [
        ('PHOTO', 'Photo'),
        ('GIF', 'Gif'),
    ]

    photo = models.TextField(blank=True, null=True)
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES, default='PHOTO')
    caption = models.TextField(blank=True, null=True)
    channels = models.ManyToManyField(ChannelModel, blank=True)

    class Meta:
        app_label = 'PostsModel'

    def __str__(self):
        return f"Post #{self.pk}"
