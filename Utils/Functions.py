import secrets
import typing

from aiogram import F
from asgiref.sync import sync_to_async
from rest_framework.exceptions import ValidationError

from ChannelModel.models import ChannelModel
from ChannelModel.serializers import ChannelSerializer
from PostsModel.serializers import PostSerializer
from UserModel.models import UserModel
from UserModel.serializers import UserSerializer


class Post:

    @staticmethod
    @sync_to_async
    def create_post(post: typing.Dict) -> bool:
        serializer = PostSerializer(data=post)
        if serializer.is_valid():
            serializer.save()
            return True
        return False


class User:

    @staticmethod
    @sync_to_async
    def get_user(user_id: int) -> UserModel:
        user_obj = UserModel.objects.get(user_id=user_id)
        return user_obj

    @staticmethod
    @sync_to_async
    def create_user(user_data: typing.Dict) -> bool:
        serializer = UserSerializer(data=user_data)
        try:
            if serializer.is_valid():
                serializer.save()
                return True
            print(serializer.errors)
            return False
        except ValidationError:
            return False

    @staticmethod
    @sync_to_async
    def update_user(user_id: int, user_data: typing.Dict) -> bool:
        user_obj = UserModel.objects.get(user_id=user_id)
        serializer = UserSerializer(user_obj, data=user_data)
        if serializer.is_valid():
            serializer.save()
            return True
        return False


class Channel:

    @staticmethod
    @sync_to_async
    def get_channel(channel_id: int) -> UserModel:
        channel_obj = ChannelModel.objects.get(channel_id=channel_id)
        return channel_obj

    @staticmethod
    @sync_to_async
    def get_related_channels(user_id: int) -> typing.List[ChannelModel]:
        user_obj = UserModel.objects.get(user_id=user_id)
        channels = ChannelModel.objects.filter(channel_holder=user_obj)
        return [i.channel_name for i in channels]

    @staticmethod
    @sync_to_async
    def create_channel(channel_data: typing.Dict) -> bool:
        serializer = ChannelSerializer(data=channel_data)
        try:
            if serializer.is_valid():
                serializer.save()
                return True
            return False
        except ValidationError:
            channel = ChannelModel.objects.get(channel_id=channel_data["channel_id"])
            try:
                user = UserModel.objects.get(pk=int(channel_data["channel_holder"]))
                return {"message": "User is holder"}
            except UserModel.DoesNotExist:
                return {"message": "Channel already exists"}

    @staticmethod
    @sync_to_async
    def get_channels_by_holder(holder_id: int) -> typing.List[ChannelModel]:
        user_pk = UserModel.objects.get(user_id=holder_id).pk
        channels = [{"name": i.channel_name, "id": i.channel_id} for i in
                    ChannelModel.objects.filter(channel_holder=user_pk)]
        return channels

    @staticmethod
    @sync_to_async
    def delete_channel_by_id(channel_id: int) -> bool:
        try:
            channel = ChannelModel.objects.get(channel_id=channel_id)
            channel.delete()
            return True
        except ChannelModel.DoesNotExist:
            return False

    @staticmethod
    @sync_to_async
    def get_channel_request_code(channel_id: int) -> str:
        channel = ChannelModel.objects.get(channel_id=channel_id)
        if channel.request_link is None:
            channel.request_link = f"{channel.channel_id}{secrets.token_urlsafe(16)}"
            channel.save()
        return channel.request_link

    @staticmethod
    @sync_to_async
    def update_request_code(channel_id: int) -> bool:
        channel = ChannelModel.objects.get(channel_id=channel_id)
        channel.request_link = f"{channel.channel_id}{secrets.token_urlsafe(16)}"
        channel.save()
        return True


class Text:
    @staticmethod
    async def get_settings_text(user_id: int) -> str:
        user_obj = await User.get_user(user_id)
        text = f'⚙️ Settings Menu\n⏳Delay: {user_obj.post_delay} minutes'
        return text

    @staticmethod
    async def get_add_channel_text(user_id: int) -> str:
        channels = "\n".join(
            [f"{index + 1}. @{i}" for index, i in enumerate(await Channel.get_related_channels(user_id))])
        if channels:
            text = f"Your bots list\n{channels}"
        else:
            text = "You don't have any channels yet"
        return text

    @staticmethod
    def is_text(text: str) -> bool:
        return F.text == text


def is_text(text: str) -> bool:
    return F.text == text
