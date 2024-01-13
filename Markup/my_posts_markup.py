from aiogram.utils.keyboard import InlineKeyboardBuilder

from Utils.classes import CallbackClasses
from Utils.functions import Post


class MyPosts:
    @staticmethod
    async def get_my_posts(user_id: int, page: int) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        posts = await Post.get_posts_by_user(user_id)
        if len(posts) == 0:
            keyboard.button(text="🔙Cancel", callback_data=CallbackClasses.QuitCallback())
            return keyboard

        keyboard.button(text="Edit channels", callback_data=CallbackClasses.QuitCallback())
        keyboard.button(text="Delete post", callback_data=CallbackClasses.QuitCallback())
        keyboard.button(text="Post now", callback_data=CallbackClasses.QuitCallback())

        if page == 1:
            keyboard.button(text="Last page", callback_data=CallbackClasses.QuitCallback())
        else:
            keyboard.button(text="Previous page", callback_data=CallbackClasses.QuitCallback())

        keyboard.button(text=f"{page}/{len(posts)}", callback_data=CallbackClasses.QuitCallback())

        if page == len(posts):
            keyboard.button(text="First page", callback_data=CallbackClasses.QuitCallback())
        else:
            keyboard.button(text="Next page", callback_data=CallbackClasses.QuitCallback())
        keyboard.button(text="🔙Cancel", callback_data=CallbackClasses.QuitCallback())

        keyboard.adjust(3, 3)
        return keyboard
