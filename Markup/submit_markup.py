from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_submit_menu() -> InlineKeyboardBuilder:
    markup = InlineKeyboardBuilder()
    markup.button(text="✅Submit", callback_data="submit")
    markup.button(text="❌Cancel", callback_data="cancel")
    return markup
