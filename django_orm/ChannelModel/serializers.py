from rest_framework import serializers

from UserModel.models import UserModel
from .models import ChannelModel


class ChannelSerializer(serializers.Serializer):
    channel_id = serializers.CharField(required=False, max_length=50, allow_blank=False, allow_null=False)
    channel_name = serializers.CharField(required=False, max_length=50, allow_blank=False, allow_null=False)
    channel_admins = serializers.CharField(read_only=True, required=False, allow_null=False)
    channel_holder = serializers.PrimaryKeyRelatedField(required=False, queryset=UserModel.objects.all())
    request_link = serializers.CharField(required=False, max_length=100, allow_blank=True, allow_null=True)
    channel_delay = serializers.IntegerField(required=False, default=15)
    delay_point = serializers.DateTimeField(required=False, allow_null=True)
    last_post = serializers.DateTimeField(required=False, allow_null=True)
    caption_template = serializers.CharField(required=False, max_length=200, allow_blank=True, allow_null=True)
    posts_number = serializers.IntegerField(required=False, default=1)
    enhance_links = serializers.BooleanField(required=False, default=True)
    active = serializers.BooleanField(required=False, default=True)

    def create(self, validated_data):
        if ChannelModel.objects.filter(channel_id=validated_data["channel_id"]).first():
            raise serializers.ValidationError({"message": "Channel with this id already exists"})
        return ChannelModel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.channel_id = validated_data.get('channel_id', instance.channel_id)
        instance.channel_name = validated_data.get('channel_name', instance.channel_name)
        instance.channel_admins = validated_data.get('channel_admins', instance.channel_admins)
        instance.channel_holder = validated_data.get('channel_holder', instance.channel_holder)
        instance.request_link = validated_data.get('request_link', instance.request_link)
        instance.channel_delay = validated_data.get('channel_delay', instance.channel_delay)
        instance.delay_point = validated_data.get('delay_point', instance.delay_point)
        instance.last_post = validated_data.get('last_post', instance.last_post)
        instance.caption_template = validated_data.get('caption_template', instance.caption_template)
        instance.posts_number = validated_data.get('posts_number', instance.posts_number)
        instance.enhance_links = validated_data.get('enhance_links', instance.enhance_links)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance
