from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InputMediaPhoto

from Markup.my_posts_markup import MyPosts
from Utils.functions import Post, Channel, Text
from loader import bot


async def my_posts_main(query: CallbackQuery):
    if isinstance(query, CallbackQuery):
        query_data = query.data.split(":")
        user_id = int(query_data[1])
        page = int(query_data[2])

        posts = await Post.get_posts_by_user(query.from_user.id)
        if len(posts) == 0:
            await query.message.delete()
            await query.answer("You have no posts")
            return
        if len(posts) < page:
            page = 1
        else:
            page = page
        post = posts[page - 1]

        keyboard = await MyPosts.get_my_posts(user_id=user_id, page=page)
        photo = InputMediaPhoto(media=post["photo"], caption=post["caption"])
        try:
            await query.message.edit_media(media=photo,
                                           reply_markup=keyboard.as_markup())
        except TelegramBadRequest:
            await query.answer()
    else:
        user_id = query.from_user.id
        page = 1
        posts = await Post.get_posts_by_user(query.from_user.id)
        if len(posts) == 0:
            await query.answer("You have no posts")
            return
        post = posts[0]
        keyboard = await MyPosts.get_my_posts(user_id=user_id, page=page)
        await query.answer_photo(photo=post["photo"], caption=post["caption"],
                                 reply_markup=keyboard.as_markup())


async def my_posts_main_back(query: CallbackQuery):
    user_id = query.from_user.id
    page = 1
    posts = await Post.get_posts_by_user(query.from_user.id)
    if len(posts) == 0:
        await query.answer("You have no posts")
        return
    post = posts[0]
    await query.message.delete()
    keyboard = await MyPosts.get_my_posts(user_id=user_id, page=page)
    await query.message.answer_photo(photo=post["photo"], caption=post["caption"],
                                     reply_markup=keyboard.as_markup())


async def delete_post_handler(query: CallbackQuery):
    query_data = query.data.split(":")
    post_id = int(query_data[3])
    result = await Post.delete_post(post_id)
    if result:
        await query.answer("Post deleted")
        await my_posts_main(query)
    else:
        await query.answer("Error")
        await my_posts_main(query)


async def post_now_handler(query: CallbackQuery):
    query_data = query.data.split(":")
    post_id = int(query_data[3])
    post = await Post.get_post(post_id)
    post_obj = await Post.get_post_obj(post_id)
    channels = post["channels"]
    failed = []
    for channel in channels:
        try:
            caption = await Text.format_caption(post["caption"], channel["id"])
            await bot.send_photo(chat_id=channel["id"], photo=post["photo"], caption=caption)
            await query.message.answer(f"Posted to {channel['name']}")
        except TelegramBadRequest:
            failed.append(channel)
            await query.answer("Error")
    channels = failed
    if len(channels) == 0:
        await Post.delete_post(post_id)
        await query.answer("Post deleted")
        await my_posts_main(query)
    else:
        await my_posts_main(query)


async def edit_channels_handler(query: CallbackQuery):
    query_data = query.data.split(":")
    user_id = int(query_data[1])
    page = int(query_data[2])
    post_id = int(query_data[3])
    await query.message.delete()
    keyboard = await MyPosts.get_edit_channels_menu(user_id=user_id, post_id=post_id, page=page)
    await query.message.answer(text="Choose channels to post to", reply_markup=keyboard.as_markup())


async def add_channel_to_post(query: CallbackQuery):
    query_data = query.data.split(":")
    user_id = int(query_data[1])
    page = int(query_data[2])
    post_id = int(query_data[3])
    channel_id = str(query_data[4])
    post = await Post.get_post(post_id)
    channels = []
    for channel in post["channels"]:
        channels += [(await Channel.get_channel(channel["id"])).pk]
    channels += [(await Channel.get_channel(channel_id)).pk]
    data = {
        "channels": channels
    }
    result = await Post.update_post(post_id, data)
    if result:
        keyboard = await MyPosts.get_edit_channels_menu(user_id=user_id, post_id=post_id, page=page)
        await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())
    else:
        await query.answer("Error")


async def remove_channel_from_post(query: CallbackQuery):
    query_data = query.data.split(":")
    user_id = int(query_data[1])
    page = int(query_data[2])
    post_id = int(query_data[3])
    channel_id = str(query_data[4])
    post = await Post.get_post(post_id)
    if len(post["channels"]) == 1:
        await query.answer("You can't remove last channel from post")
        return
    channels = []
    for channel in post["channels"]:
        if channel["id"] != channel_id:
            channels += [(await Channel.get_channel(channel["id"])).pk]
    data = {
        "channels": channels
    }
    result = await Post.update_post(post_id, data)
    if result:
        keyboard = await MyPosts.get_edit_channels_menu(user_id=user_id, post_id=post_id, page=page)
        await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())
    else:
        await query.answer("Error")
