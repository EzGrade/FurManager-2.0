from aiogram.types import CallbackQuery

from Markup.my_posts_markup import MyPosts
from Utils.functions import Post


async def my_posts_main(query: CallbackQuery):
    if isinstance(query, CallbackQuery):
        query_data = query.data.split(":")
        user_id = int(query_data[1])
        page = int(query_data[2])
        posts = await Post.get_posts_by_user(query.from_user.id)
        post = posts[0]
        keyboard = await MyPosts.get_my_posts(user_id=user_id, page=page)
        await query.message.answer_photo(photo=post.photo, caption=post.caption,
                                         reply_markup=keyboard.as_markup())
    else:
        user_id = query.from_user.id
        page = 1
        posts = await Post.get_posts_by_user(query.from_user.id)
        post = posts[0]
        keyboard = await MyPosts.get_my_posts(user_id=user_id, page=page)
        await query.answer_photo(photo=post["photo"], caption=post["caption"],
                                 reply_markup=keyboard.as_markup())
