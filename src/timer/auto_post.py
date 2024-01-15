import os
from datetime import datetime, timezone, UTC

import django
from asgiref.sync import sync_to_async
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

settings.configure(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "furmanager",
            "USER": "postgres",
            "PASSWORD": "GradeTop1!",
            "HOST": "localhost",
            "PORT": "5432",
        }
    },
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'PostsModel.apps.PostsmodelConfig',
        'UserModel.apps.UsermodelConfig',
        'ChannelModel.apps.ChannelmodelConfig',
    ]
)

django.setup()

from ChannelModel.models import ChannelModel
from PostsModel.models import PostsModel

import time
import asyncio

from loader import bot
from Utils.functions import Text


class AutoPost:
    def __init__(self):
        self.channels = []
        self.bot = bot

    def __UpdateChannels(self):
        self.channels = ChannelModel.objects.filter(active=True)

    def __GetChannels(self):
        self.__UpdateChannels()
        return [channel.channel_id for channel in self.channels]

    async def __SendPost(self, channel_id: int, image: str, text: str):
        await self.bot.send_photo(chat_id=channel_id, photo=image, caption=text, parse_mode="MarkdownV2")
        await self.__UpdateLastPost(channel_id)

    @sync_to_async
    def __GetChannelStartPoint(self, channel_id: int):
        channel = ChannelModel.objects.get(channel_id=channel_id)
        return self.__DateTimeToUnix(channel.delay_point)

    @sync_to_async
    def __GetLastPost(self, channel_id: int):
        channel = ChannelModel.objects.get(channel_id=channel_id)
        if channel.last_post is None:
            return None
        return self.__DateTimeToUnix(channel.last_post)

    @staticmethod
    @sync_to_async
    def __UpdateLastPost(channel_id: int):
        channel = ChannelModel.objects.get(channel_id=channel_id)
        channel.last_post = datetime.now(UTC)
        channel.save()

    @staticmethod
    @sync_to_async
    def __GetPost(channel_id: int) -> PostsModel:
        return PostsModel.objects.filter(channels__channel_id__contains=channel_id).first()

    @staticmethod
    def __DateTimeToUnix(dt):
        return int(dt.replace(tzinfo=timezone.utc).timestamp())

    def __GetCurrentTime(self):
        return self.__DateTimeToUnix(datetime.now(timezone.utc))

    @staticmethod
    @sync_to_async
    def __MinutesToUnix(channel_id: int):
        channel = ChannelModel.objects.get(channel_id=channel_id)
        return channel.channel_delay * 60

    @staticmethod
    @sync_to_async
    def __RemoveChannel(channel_id: int, post: PostsModel):
        channel_obj = ChannelModel.objects.get(channel_id=channel_id)
        post.channels.remove(channel_obj)
        post.save()
        if len(post.channels.all()) == 0:
            post.delete()

    async def __Run(self, channels: list = None):
        tasks = []
        for channel in channels:
            last_post = await self.__GetLastPost(channel)
            start_point = await self.__GetChannelStartPoint(channel)
            channel_delay = await self.__MinutesToUnix(channel)
            to_compare = last_post if last_post is not None else start_point
            if self.__GetCurrentTime() - to_compare < channel_delay:
                continue

            post = await self.__GetPost(channel)
            if post is not None:
                caption = await Text.format_caption(post.caption, channel)
                task = asyncio.create_task(self.__SendPost(channel, post.photo, caption))
                tasks.append(task)
                await self.__RemoveChannel(channel, post)

        await asyncio.gather(*tasks)

    def Start(self):
        while True:
            channels = self.__GetChannels()
            asyncio.get_event_loop().run_until_complete(self.__Run(channels=channels))
            time.sleep(5)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    AutoPost().Start()
