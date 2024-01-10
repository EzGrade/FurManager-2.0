from rest_framework import serializers

from .models import UserModel


class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)
    user_name = serializers.CharField(required=False)
    post_delay = serializers.IntegerField(required=False)
    channel_id = serializers.ListField(child=serializers.IntegerField(), required=False)

    def create(self, validated_data):
        if UserModel.objects.filter(user_id=validated_data['user_id']).exists():
            raise serializers.ValidationError("User with this ID already exists.")
        return UserModel.objects.create(**validated_data)

    class Meta:
        model = UserModel
        fields = '__all__'
