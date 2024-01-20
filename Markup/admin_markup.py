from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import KeyboardBuilder

from Utils.classes import CallbackClasses


class AdminMenu:
    @staticmethod
    async def get_main_menu(
            user_id: int
    ) -> KeyboardBuilder:
        keyboard = KeyboardBuilder(KeyboardButton)
        keyboard.button(text="Global Message", callback_data=CallbackClasses.AdminPanel.GlobalMessage(
            user_id=user_id
        ))
        return keyboard
