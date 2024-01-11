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
        instance.save()
        return instance
