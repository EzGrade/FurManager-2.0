import datetime
import re
import secrets
import typing

from aiogram import F
from asgiref.sync import sync_to_async
from rest_framework.exceptions import ValidationError
from tldextract import extract

from ChannelModel.models import ChannelModel
from ChannelModel.serializers import ChannelSerializer
from PostsModel.models import PostsModel
from PostsModel.serializers import PostSerializer
from UserModel.models import UserModel
from UserModel.serializers import UserSerializer
from loader import bot


class Post:

    @staticmethod
    @sync_to_async
    def create_post(
            post: typing.Dict
    ) -> bool:
        """
        Asynchronously creates a post using the provided data.

        This method takes a dictionary representing a post, validates it using the PostSerializer,
        and if valid, saves it to the database. If the post is successfully saved, it returns the
        instance of the saved post. If the post is not valid, it returns False.

        Parameters:
        post (typing.Dict): A dictionary containing the data for the post to be created.

        Returns:
        bool: True if the post was successfully created and saved, False otherwise.
        """
        serializer = PostSerializer(
            data=post
        )
        if serializer.is_valid():
            serializer.save()
            return serializer.instance
        return False

    @staticmethod
    @sync_to_async
    def set_channels(
            post_id: int,
            channels: typing.List[int]
    ) -> bool:
        """
        Asynchronously sets the channels for a specific post.

        This method takes a post ID and a list of channel IDs. It retrieves the post
        corresponding to the given post ID and sets its channels to the provided list of channel IDs.

        Parameters:
        post_id (int): The ID of the post to update.
        channels (typing.List[int]): A list of channel IDs to set for the post.

        Returns:
        bool: True if the operation was successful, False otherwise.
        """
        post = PostSerializer(
            instance=PostsModel.objects.get(
                pk=post_id
            ))
        post.instance.channels.set(channels)
        return True

    @staticmethod
    @sync_to_async
    def get_posts_by_user(
            user_id: int
    ) -> PostsModel:
        """
        Asynchronously retrieves all posts associated with a specific user.

        This method takes a user ID, retrieves the user object associated with that ID, and then
        retrieves all posts associated with the channels that the user is part of. It returns a list
        of dictionaries, each representing a post.

        Parameters:
        user_id (int): The ID of the user whose posts are to be retrieved.

        Returns:
        list[dict]: A list of dictionaries, each representing a post. Each dictionary contains the
        post's primary key, photo, media type, caption, and associated channels.
        """
        user_obj = UserModel.objects.get(
            user_id=user_id
        )
        result = []
        for channel in user_obj.channel_id:
            posts = PostsModel.objects.filter(
                channels__channel_id__contains=channel
            )
            for post in posts:
                post_json = {
                    "pk": post.pk,
                    "photo": post.photo,
                    "media_type": post.media_type,
                    "caption": post.caption,
                    "channels": post.channels
                }
                if post_json not in result:
                    result.append(post_json)
        return result

    @staticmethod
    @sync_to_async
    def delete_post(
            post_id: int
    ) -> bool:
        """
        Asynchronously deletes a post by its ID.

        This method attempts to retrieve a post by its ID and delete it.
        If the post is successfully deleted, it returns True.
        If the post does not exist, it returns False.

        Parameters:
        post_id (int): The ID of the post to be deleted.

        Returns:
        bool: True if the post was successfully deleted, False otherwise.
        """
        try:
            post = PostsModel.objects.get(
                pk=post_id
            )
            post.delete()
            return True
        except PostsModel.DoesNotExist:
            return False

    @staticmethod
    @sync_to_async
    def get_post(
            post_id: int
    ) -> PostsModel:
        """
        Asynchronously retrieves a post by its ID and its associated channels.

        This method takes a post ID, retrieves the post object associated with that ID, and then
        retrieves all channels associated with the post. It returns a dictionary representing the post
        and its associated channels.

        Parameters:
        post_id (int): The ID of the post to be retrieved.

        Returns:
        dict: A dictionary representing the post. The dictionary contains the post's primary key, photo,
        media type, caption, and a list of dictionaries each representing a channel associated with the post.
        Each channel dictionary contains the channel's name and ID.
        """
        post = PostsModel.objects.get(
            pk=post_id
        )
        channels = [
            {
                "name": i.channel_name,
                "id": i.channel_id
            } for i in post.channels.all()]
        return {
            "pk": post.pk,
            "photo": post.photo,
            "media_type": post.media_type,
            "caption": post.caption,
            "channels": channels
        }

    @staticmethod
    @sync_to_async
    def update_post(
            post_id: int,
            post_data: typing.Dict
    ) -> bool:
        """
        Asynchronously updates a post with the provided data.

        This method takes a post ID and a dictionary representing the new data for the post.
        It retrieves the post object associated with the given ID and updates it with the new data.
        If the new data is valid, it saves the updated post and returns True. If the new data is not valid, it returns False.

        Parameters:
        post_id (int): The ID of the post to be updated.
        post_data (typing.Dict): A dictionary containing the new data for the post.

        Returns:
        bool: True if the post was successfully updated and saved, False otherwise.
        """
        post_obj = PostsModel.objects.get(
            pk=post_id
        )
        serializer = PostSerializer(
            instance=post_obj,
            data=post_data
        )
        if serializer.is_valid():
            serializer.update(
                instance=post_obj,
                validated_data=post_data
            )
            return True
        return False

    @staticmethod
    @sync_to_async
    def get_post_obj(
            post_id: int
    ) -> PostsModel:
        """
        Asynchronously retrieves a post object by its ID.

        This method takes a post ID and retrieves the post object associated with that ID from the database.

        Parameters:
        post_id (int): The ID of the post to be retrieved.

        Returns:
        PostsModel: The post object associated with the given ID.
        """
        return PostsModel.objects.get(
            pk=post_id
        )


class User:

    @staticmethod
    @sync_to_async
    def get_user(
            user_id: int
    ) -> UserModel:
        """
        Asynchronously retrieves a user object by its ID.

        This method takes a user ID and retrieves the user object associated with that ID from the database.

        Parameters:
        user_id (int): The ID of the user to be retrieved.

        Returns:
        UserModel: The user object associated with the given ID.
        """
        user_obj = UserModel.objects.get(
            user_id=user_id
        )
        return user_obj

    @staticmethod
    @sync_to_async
    def create_user(
            user_data: typing.Dict
    ) -> bool:
        serializer = UserSerializer(
            data=user_data
        )
        try:
            if serializer.is_valid():
                serializer.save()
                return True
            return False
        except ValidationError:
            return False

    @staticmethod
    @sync_to_async
    def update_user(
            user_id: int,
            user_data: typing.Dict
    ) -> bool:
        user_obj = UserModel.objects.get(
            user_id=user_id
        )
        serializer = UserSerializer(
            instance=user_obj,
            data=user_data
        )
        if serializer.is_valid():
            serializer.save()
            return True
        return False

    @staticmethod
    @sync_to_async
    def get_user_by_channel(
            channel: int
    ) -> UserModel:
        user = UserModel.objects.get(
            pk=channel.channel_holder.pk
        )
        return user

    @staticmethod
    @sync_to_async
    def get_all_user_ids() -> typing.List[int]:
        users = UserModel.objects.all()
        ids = [i.user_id for i in users]
        return ids


class Channel:

    @staticmethod
    @sync_to_async
    def get_channel(
            channel_id: int
    ) -> ChannelModel:
        channel_obj = ChannelModel.objects.get(
            channel_id=channel_id
        )
        return channel_obj

    @staticmethod
    @sync_to_async
    def create_channel(
            channel_data: typing.Dict
    ) -> bool:
        serializer = ChannelSerializer(
            data=channel_data
        )
        try:
            if serializer.is_valid():
                serializer.save()
                user = UserModel.objects.get(
                    pk=int(channel_data["channel_holder"])
                )
                user.channel_id += [channel_data["channel_id"]]
                user.save()
                return True
            return False
        except ValidationError as e:
            channel = ChannelModel.objects.get(
                channel_id=channel_data["channel_id"]
            )
            try:
                user = UserModel.objects.get(
                    pk=int(channel_data["channel_holder"])
                )
                return {"message": "User is holder"}
            except UserModel.DoesNotExist:
                return {"message": "Channel already exists"}

    @staticmethod
    @sync_to_async
    def update_channel(
            channel_id: int,
            channel_data: typing.Dict
    ) -> bool:
        channel_obj = ChannelModel.objects.get(
            channel_id=channel_id
        )
        serializer = ChannelSerializer(
            instance=channel_obj,
            data=channel_data
        )
        if serializer.is_valid():
            serializer.update(
                instance=channel_obj,
                validated_data=channel_data
            )
            return True
        return False

    @staticmethod
    @sync_to_async
    def get_channels_by_holder(
            holder_id: int
    ) -> typing.List[ChannelModel]:
        user = UserModel.objects.get(
            user_id=holder_id
        )
        user_pk = user.pk
        channels = [
            {
                "name": i.channel_name,
                "id": i.channel_id
            } for i in
            ChannelModel.objects.filter(channel_holder=user_pk)]
        return channels

    @staticmethod
    @sync_to_async
    def delete_channel_by_id(
            channel_id: int
    ) -> bool:
        try:
            channel = ChannelModel.objects.get(
                channel_id=channel_id
            )
            for user_id in channel.channel_admins:
                user = UserModel.objects.get(
                    user_id=user_id
                )
                user.channel_id.remove(channel_id)
                user.save()
            channel_holder = UserModel.objects.get(
                pk=channel.channel_holder.pk
            )
            channel_holder.channel_id.remove(channel_id)
            channel_holder.save()
            channel.delete()
            return True
        except ChannelModel.DoesNotExist:
            return False

    @staticmethod
    @sync_to_async
    def get_channel_request_code(
            channel_id: int
    ) -> str:
        channel = ChannelModel.objects.get(
            channel_id=channel_id
        )
        if channel.request_link is None:
            channel.request_link = f"{channel.channel_id[1:]}{secrets.token_urlsafe(16)}"
            channel.save()
        return channel.request_link

    @staticmethod
    @sync_to_async
    def update_request_code(
            channel_id: int
    ) -> bool:
        channel = ChannelModel.objects.get(
            channel_id=channel_id
        )
        channel.request_link = f"{channel.channel_id[1:]}{secrets.token_urlsafe(16)}"
        channel.save()
        return True

    @staticmethod
    @sync_to_async
    def get_channel_by_request_code(
            request_code: str
    ) -> ChannelModel:
        try:
            channel = ChannelModel.objects.get(
                request_link=request_code
            )
            return channel
        except ChannelModel.DoesNotExist:
            return False

    @staticmethod
    @sync_to_async
    def add_admin(
            user_id: int,
            channel_id: int
    ) -> bool:
        try:
            channel = ChannelModel.objects.get(
                channel_id=channel_id
            )
            channel.channel_admins += [user_id]
            channel.save()
            return True
        except ChannelModel.DoesNotExist:
            return False

    @staticmethod
    @sync_to_async
    def get_channels_by_admin(
            admin_id: int
    ) -> typing.List[ChannelModel]:
        channels = ChannelModel.objects.filter(
            channel_admins__contains=[admin_id]
        )
        channels = [
            {
                "name": i.channel_name,
                "id": i.channel_id
            } for i in channels]
        return channels

    @staticmethod
    @sync_to_async
    def get_admins_by_channel(
            channel_id: int
    ) -> typing.List[UserModel]:
        channel = ChannelModel.objects.get(
            channel_id=channel_id
        )
        admins = [
            {
                "name": UserModel.objects.get(user_id=i).user_name,
                "id": UserModel.objects.get(user_id=i).user_id
            } for i in channel.channel_admins]
        return admins

    @staticmethod
    @sync_to_async
    def remove_admin(
            user_id: int,
            channel_id: int,
            admin_id: int
    ) -> bool:
        try:
            channel = ChannelModel.objects.get(
                channel_id=channel_id
            )
            if user_id == channel.channel_holder.user_id:
                channel.channel_admins.remove(admin_id)
                channel.save()
                admin = UserModel.objects.get(
                    user_id=admin_id
                )
                admin.channel_id.remove(channel_id)
                admin.save()
                return True
            return False
        except ChannelModel.DoesNotExist or UserModel.DoesNotExist:
            return False

    @staticmethod
    @sync_to_async
    def get_current_delay(
            channel_id: int
    ) -> int:
        channel = ChannelModel.objects.get(
            channel_id=channel_id
        )
        return channel.channel_delay

    @staticmethod
    @sync_to_async
    def filter_activated(
            channels_id: typing.List[int]
    ) -> typing.List[ChannelModel]:
        channels = ChannelModel.objects.filter(
            channel_id__in=channels_id
        )
        result = [i.channel_id for i in channels if i.active]
        return result

    @staticmethod
    @sync_to_async
    def get_channels_by_user_id(
            user_id: int
    ) -> typing.List[ChannelModel]:
        user = UserModel.objects.get(
            user_id=user_id
        )
        channels_admin = ChannelModel.objects.filter(
            channel_admins__contains=[user_id]
        )
        channels_holder = ChannelModel.objects.filter(
            channel_holder=user
        )
        channels = list(set(channels_admin) | set(channels_holder))
        return channels


class Text:
    @staticmethod
    async def get_settings_text(
            user_id: int
    ) -> str:
        user_obj = await User.get_user(user_id)
        text = f'⚙️ Settings Menu\nBots number: {len(user_obj.channel_id)}'
        return text

    @staticmethod
    async def get_channel_settings_text(
            channel_id: int
    ) -> str:
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
        next_post = "" if not next_post else next_post.strftime(date_format)
        text = (f'⚙️ Channel Settings Menu\n\n'
                f'⌨️Name: {channel_obj.channel_name}\n'
                f'🆔ID: {channel_id}\n\n'
                f'⏳Delay Options\n'
                f'  ⏳Delay: {channel_obj.channel_delay}\n'
                f'  🏁Delay start point: {date}\n\n'
                f'ℹ️Post Info\n'
                f'  📊Posts number: {channel_obj.posts_number}\n'
                f'  📅Last post: {last_post}\n'
                f'  📅Next post: {next_post}\n\n'
                f'  📋Template: {channel_obj.caption_template}\n'
                f'👥Admins:\n{admins_text}\n\n'
                f'Active: {"✅" + str(channel_obj.active) if channel_obj.active else "❌" + str(channel_obj.active)}\n'
                f'Enhance links: {"✅" + str(channel_obj.enhance_links) if channel_obj.enhance_links else "❌" + str(channel_obj.enhance_links)}\n\n')
        return text

    @staticmethod
    async def get_delay_text(
            channel_id: int
    ) -> str:
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
        next_post = "" if not next_post else next_post.strftime(date_format)
        text = (f'⚙️ Delay Menu\n\n'
                f'⏳Delay Options\n'
                f'  ⏳Delay: {channel_obj.channel_delay}\n'
                f'  🏁Delay start point: {date}\n\n'
                f'ℹ️Post Info\n'
                f'  📋Template: {channel_obj.caption_template}\n'
                f'  📊Posts number: {channel_obj.posts_number}\n'
                f'  📅Last post: {last_post}\n'
                f'  📅Next post: {next_post}\n\n')
        return text

    @staticmethod
    async def get_add_channel_text(
            user_id: int
    ) -> str:
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
    async def template_text(
            channel_id: int
    ) -> str:
        channel_obj = await Channel.get_channel(channel_id)
        current_template = channel_obj.caption_template
        if current_template is None:
            current_template = "No template"

        help_text = ("You can use\n"
                     "  ```%text%```post caption\n"
                     "  ```%channel name%```channel name\n"
                     "  ```%channel id%```channel id\n"
                     "  ```%channel link%```channel link\n\n")

        text = f"📋{help_text}✅Current template\n{current_template}"
        return text

    @staticmethod
    def process_template(
            text: str
    ) -> list[str] | None:
        import re
        pattern = r'%([^%]+)%'
        matches = re.findall(pattern, text)
        warning = []
        for match in matches:
            if match not in ["text", "channel name", "channel id", "channel link"]:
                warning.append(match)
        if warning:
            return warning

    @staticmethod
    def process_caption_links(text: str) -> str:
        text = text.replace("\.", ".")
        url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        urls = re.findall(url_pattern, text)
        for url in urls:
            extract_result = extract(url)
            td = extract_result.domain
            text = text.replace(url, f'[{td.capitalize()}]({url})')
        return text

    @staticmethod
    @sync_to_async
    def format_caption(
            caption_str: str | None,
            channel_id: int
    ) -> str:
        channel = ChannelModel.objects.get(channel_id=channel_id)
        template = channel.caption_template
        if template is None:
            if channel.enhance_links:
                caption_str = Text.process_caption_links(caption_str)
            return caption_str
        if "%text%" in template:
            if caption_str is not None:
                if channel.enhance_links:
                    caption_str = Text.process_caption_links(caption_str)
                template = template.replace("%text%", caption_str)
            else:
                template = template.replace("%text%", "")
        if "%channel name%" in template:
            template = template.replace("%channel name%", channel.channel_name)
        if "%channel id%" in template:
            template = template.replace("%channel id%", channel.channel_id)
        if "%channel link%" in template:
            if channel.channel_name:
                template = template.replace("%channel link%",
                                            f"[{channel.channel_name}](https://t.me/{channel.channel_name})")
            else:
                template = template.replace("%channel link%", f"[Channel Link](https://t.me/{channel.channel_id})")

        return template

    @staticmethod
    @sync_to_async
    def get_posts_number_text(
            channel_id: int
    ) -> str:
        channel = ChannelModel.objects.get(
            channel_id=channel_id
        )
        text = (f"⚙️Posts number edit menu\n"
                f"ℹ️Change number of posts that will be posted at the same time")
        return text

    @staticmethod
    def is_text(
            text: str
    ) -> bool:
        return F.text == text

    @staticmethod
    @sync_to_async
    def admin_panel_text() -> str:
        users_number = UserModel.objects.count()
        channels_number = ChannelModel.objects.count()
        posts_number = PostsModel.objects.count()
        post_per_user = posts_number / users_number
        post_per_channel = posts_number / channels_number
        channel_per_user = channels_number / users_number
        text = (
            f"📊Admin panel\n"
            f"ℹ️Users number: {users_number}\n"
            f"  ℹ️Posts per user: {post_per_user}\n"
            f"  ℹ️Channels per user: {channel_per_user}\n"
            f"ℹ️Posts number: {posts_number}\n"
            f"  ℹ️Posts per channel: {post_per_channel}\n"
            f"ℹ️Channels number: {channels_number}\n"
        )
        return text


class Telegram:
    @staticmethod
    async def get_link(chat_id: int) -> str:
        chat = await bot.get_chat(chat_id=chat_id)
        return chat.type


async def test():
    print(await Telegram.get_link(-1002069224843))
