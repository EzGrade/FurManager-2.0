import datetime
import secrets
import typing

from aiogram import F
from asgiref.sync import sync_to_async
from rest_framework.exceptions import ValidationError

from ChannelModel.models import ChannelModel
from ChannelModel.serializers import ChannelSerializer
from PostsModel.models import PostsModel
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
            return serializer.instance
        return False

    @staticmethod
    @sync_to_async
    def set_channels(post_id: int, channels: typing.List[int]) -> bool:
        post = PostSerializer(PostsModel.objects.get(pk=post_id))
        post.instance.channels.set(channels)
        return True

    @staticmethod
    @sync_to_async
    def get_posts_by_user(user_id: int) -> PostsModel:
        user_obj = UserModel.objects.get(user_id=user_id)
        result = []
        for channel in user_obj.channel_id:
            posts = PostsModel.objects.filter(channels__channel_id__contains=channel)
            for post in posts:
                post_json = {"pk": post.pk, "photo": post.photo, "caption": post.caption, "channels": post.channels}
                if post_json not in result:
                    result.append(post_json)
        return result

    @staticmethod
    @sync_to_async
    def delete_post(post_id: int) -> bool:
        try:
            post = PostsModel.objects.get(pk=post_id)
            post.delete()
            return True
        except PostsModel.DoesNotExist:
            return False

    @staticmethod
    @sync_to_async
    def get_post(post_id: int) -> PostsModel:
        post = PostsModel.objects.get(pk=post_id)
        channels = [{"name": i.channel_name, "id": i.channel_id} for i in post.channels.all()]
        return {"pk": post.pk, "photo": post.photo, "caption": post.caption, "channels": channels}

    @staticmethod
    @sync_to_async
    def update_post(post_id: int, post_data: typing.Dict) -> bool:
        post_obj = PostsModel.objects.get(pk=post_id)
        serializer = PostSerializer(post_obj, data=post_data)
        if serializer.is_valid():
            serializer.update(post_obj, post_data)
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

    @staticmethod
    @sync_to_async
    def get_user_by_channel(channel: int) -> UserModel:
        user = UserModel.objects.get(pk=channel.channel_holder.pk)
        return user


class Channel:

    @staticmethod
    @sync_to_async
    def get_channel(channel_id: int) -> ChannelModel:
        channel_obj = ChannelModel.objects.get(channel_id=channel_id)
        return channel_obj

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
    def update_channel(channel_id: int, channel_data: typing.Dict) -> bool:
        channel_obj = ChannelModel.objects.get(channel_id=channel_id)
        serializer = ChannelSerializer(channel_obj, data=channel_data)
        if serializer.is_valid():
            serializer.update(channel_obj, channel_data)
            return True
        print(serializer.errors)
        return False

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
            for user_id in channel.channel_admins:
                user = UserModel.objects.get(user_id=user_id)
                user.channel_id.remove(channel_id)
                user.save()
            channel_holder = UserModel.objects.get(pk=channel.channel_holder.pk)
            channel_holder.channel_id.remove(channel_id)
            channel_holder.save()
            channel.delete()
            return True
        except ChannelModel.DoesNotExist:
            return False

    @staticmethod
    @sync_to_async
    def get_channel_request_code(channel_id: int) -> str:
        channel = ChannelModel.objects.get(channel_id=channel_id)
        if channel.request_link is None:
            channel.request_link = f"{channel.channel_id[1:]}{secrets.token_urlsafe(16)}"
            channel.save()
        return channel.request_link

    @staticmethod
    @sync_to_async
    def update_request_code(channel_id: int) -> bool:
        channel = ChannelModel.objects.get(channel_id=channel_id)
        channel.request_link = f"{channel.channel_id[1:]}{secrets.token_urlsafe(16)}"
        channel.save()
        return True

    @staticmethod
    @sync_to_async
    def get_channel_by_request_code(request_code: str) -> ChannelModel:
        try:
            channel = ChannelModel.objects.get(request_link=request_code)
            return channel
        except ChannelModel.DoesNotExist:
            return False

    @staticmethod
    @sync_to_async
    def add_admin(user_id: int, channel_id: int) -> bool:
        try:
            channel = ChannelModel.objects.get(channel_id=channel_id)
            channel.channel_admins += [user_id]
            channel.save()
            return True
        except ChannelModel.DoesNotExist:
            return False

    @staticmethod
    @sync_to_async
    def get_channels_by_admin(admin_id: int) -> typing.List[ChannelModel]:
        channels = ChannelModel.objects.filter(channel_admins__contains=[admin_id])
        channels = [{"name": i.channel_name, "id": i.channel_id} for i in
                    channels]
        return channels

    @staticmethod
    @sync_to_async
    def get_admins_by_channel(channel_id: int) -> typing.List[UserModel]:
        channel = ChannelModel.objects.get(channel_id=channel_id)
        admins = [{"name": UserModel.objects.get(user_id=i).user_name, "id": UserModel.objects.get(user_id=i).user_id}
                  for i in channel.channel_admins]
        return admins

    @staticmethod
    @sync_to_async
    def remove_admin(user_id: int, channel_id: int, admin_id: int) -> bool:
        try:
            channel = ChannelModel.objects.get(channel_id=channel_id)
            if user_id == channel.channel_holder.user_id:
                channel.channel_admins.remove(admin_id)
                channel.save()
                admin = UserModel.objects.get(user_id=admin_id)
                admin.channel_id.remove(channel_id)
                admin.save()
                return True
            return False
        except ChannelModel.DoesNotExist or UserModel.DoesNotExist:
            return False

    @staticmethod
    @sync_to_async
    def get_current_delay(channel_id: int) -> int:
        channel = ChannelModel.objects.get(channel_id=channel_id)
        return channel.channel_delay

    @staticmethod
    @sync_to_async
    def filter_activated(channels_id: typing.List[int]) -> typing.List[ChannelModel]:
        channels = ChannelModel.objects.filter(channel_id__in=channels_id)
        result = [i.channel_id for i in channels if i.active]
        return result

    @staticmethod
    @sync_to_async
    def get_channels_by_user_id(user_id: int) -> typing.List[ChannelModel]:
        user = UserModel.objects.get(user_id=user_id)
        channels_admin = ChannelModel.objects.filter(channel_admins__contains=[user_id])
        channels_holder = ChannelModel.objects.filter(channel_holder=user)
        channels = list(set(channels_admin) | set(channels_holder))
        return channels


class Text:
    @staticmethod
    async def get_settings_text(user_id: int) -> str:
        user_obj = await User.get_user(user_id)
        text = f'⚙️ Settings Menu\nBots number: {len(user_obj.channel_id)}'
        return text

    @staticmethod
    async def get_channel_settings_text(channel_id: int) -> str:
        channel_obj = await Channel.get_channel(channel_id)
        admins = await Channel.get_admins_by_channel(channel_id)
        admins_text = []
        for index, admin in enumerate(admins):
            admins_text += [f"      {index + 1}. {admin['name']} - {admin['id']}"]
        admins_text = "\n".join(admins_text)
        date_format = "%Y-%m-%d %H:%M"
        date = channel_obj.delay_point.strftime(date_format)
        last_post = channel_obj.last_post.strftime(date_format) if channel_obj.last_post else ""
        if channel_obj.last_post:
            next_post = channel_obj.last_post + datetime.timedelta(
                minutes=channel_obj.channel_delay) if channel_obj.last_post else ""
        else:
            next_post = channel_obj.delay_point + datetime.timedelta(
                minutes=channel_obj.channel_delay) if channel_obj.delay_point else ""
        next_post = next_post.strftime(date_format) if next_post else ""
        text = (f'⚙️ Channel Settings Menu\n\n'
                f'⌨️Name: {channel_obj.channel_name}\n'
                f'🆔ID: {channel_id}\n\n'
                f'⏳Delay Options\n'
                f'  ⏳Delay: {channel_obj.channel_delay}\n'
                f'  🏁Delay start point: {date}\n\n'
                f'ℹ️Post Info\n'
                f'  📅Last post: {last_post}\n'
                f'  📅Next post: {next_post}\n\n'
                f'👥Admins:\n{admins_text}\n\n'
                f'Active: {"✅" + str(channel_obj.active) if channel_obj.active else "❌" + str(channel_obj.active)}\n')
        return text

    @staticmethod
    async def get_delay_text(channel_id: int) -> str:
        channel_obj = await Channel.get_channel(channel_id)
        date_format = "%Y-%m-%d %H:%M"
        date = channel_obj.delay_point.strftime(date_format)
        last_post = channel_obj.last_post.strftime(date_format) if channel_obj.last_post else ""
        if channel_obj.last_post:
            next_post = channel_obj.last_post + datetime.timedelta(
                minutes=channel_obj.channel_delay) if channel_obj.last_post else ""
        else:
            next_post = channel_obj.delay_point + datetime.timedelta(
                minutes=channel_obj.channel_delay) if channel_obj.delay_point else ""
        next_post = next_post.strftime(date_format) if next_post else ""
        text = (f'⚙️ Delay Menu\n\n'
                f'⏳Delay Options\n'
                f'  ⏳Delay: {channel_obj.channel_delay}\n'
                f'  🏁Delay start point: {date}\n\n'
                f'ℹ️Post Info\n'
                f'  📅Last post: {last_post}\n'
                f'  📅Next post: {next_post}\n')
        return text

    @staticmethod
    async def get_add_channel_text(user_id: int) -> str:
        channels = await Channel.get_channels_by_holder(user_id)
        channels_holder_list = channels
        channels_holder = "\n".join(
            [f"{index + 1}. @{i['name']}" for index, i in enumerate(channels)])
        channels = await Channel.get_channels_by_admin(user_id)
        channels_admin_list = []
        for i in channels:
            if i not in channels_holder_list:
                channels_admin_list.append(i)
        channels_admin = "\n".join(
            [f"{index + 1}. @{i['name']}" for index, i in enumerate(channels_admin_list)])

        if channels_holder or channels_admin:
            text = f"Your bots list\n- You are holder in: \n{channels_holder}\n- You are admin in: \n{channels_admin}"
        else:
            text = "You don't have any channels yet"
        return text

    @staticmethod
    def is_text(text: str) -> bool:
        return F.text == text


def is_text(text: str) -> bool:
    return F.text == text
