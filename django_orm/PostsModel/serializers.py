from rest_framework import serializers

from ChannelModel.models import ChannelModel
from .models import PostsModel


class PostSerializer(serializers.ModelSerializer):
    photo = serializers.CharField(allow_blank=True, allow_null=True)
    caption = serializers.CharField(allow_blank=True, allow_null=True)
    channels = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=ChannelModel.objects.all(),
                                                  required=False)

    def create(self, validated_data):
        return PostsModel.objects.create(**validated_data)

    class Meta:
        model = PostsModel
        fields = '__all__'
