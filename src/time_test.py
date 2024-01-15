from loader import bot
import asyncio


async def test_markdown(message):
    await bot.send_message(chat_id=1019900002,
                           text='[testchannelgrade](https://t.me/testchannelgrade)',
                           parse_mode="MarkdownV2")

asyncio.run(test_markdown(1))