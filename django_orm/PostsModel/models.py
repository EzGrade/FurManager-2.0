from django.db import models
from UserModel.models import UserModel


# Create your models here.
class PostsModel(models.Model):
    photo = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=150, blank=True, null=True)
    tags = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(UserModel, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        app_label = 'PostsModel'

    def __str__(self):
        return f"Post #{self.pk}"
