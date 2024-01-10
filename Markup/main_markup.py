from aiogram.utils.keyboard import KeyboardBuilder, KeyboardButton


def get_main_menu():
    markup = KeyboardBuilder(KeyboardButton)
    markup.button(text="➕Create post", callback_data="create_post")
    markup.button(text="📋My posts", callback_data="my_posts")
    markup.button(text="⚙️Settings", callback_data="settings")
    return markup
