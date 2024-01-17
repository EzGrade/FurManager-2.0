import asyncio

import app
from timer.auto_post import AutoPost


async def main():
    auto_post = AutoPost()
    await asyncio.gather(
        AutoPost().Start(),
        app.run()
    )


if __name__ == '__main__':
    asyncio.run(main())
