import asyncio
from datetime import datetime, timezone, UTC

from asgiref.sync import sync_to_async

from ChannelModel.models import ChannelModel
from PostsModel.models import PostsModel
from Utils.functions import Text
from loader import bot


class AutoPost:
    def __init__(self):
        self.channels = []
        self.bot = bot

    def __UpdateChannels(self):
        self.channels = ChannelModel.objects.filter(active=True)

    @sync_to_async
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

    async def Start(self):
        print("Auto Posting Started...")
        while True:
            channels = await self.__GetChannels()
            await self.__Run(channels=channels)
            await asyncio.sleep(5)


def Run():
    print("Starting Auto Posting...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(AutoPost().Start)


if __name__ == '__main__':
    print("Starting Auto Posting...")
    AutoPost().Run()
