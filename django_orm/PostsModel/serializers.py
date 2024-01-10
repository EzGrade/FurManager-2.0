from rest_framework import serializers

from UserModel.models import UserModel
from .models import PostsModel


class PostSerializer(serializers.ModelSerializer):
    photo = serializers.CharField(allow_blank=True, allow_null=True)
    author = serializers.CharField(allow_blank=True, allow_null=True)
    tags = serializers.CharField(allow_blank=True, allow_null=True)
    user = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all())

    def create(self, validated_data):
        return PostsModel.objects.create(**validated_data)

    class Meta:
        model = PostsModel
        fields = '__all__'
