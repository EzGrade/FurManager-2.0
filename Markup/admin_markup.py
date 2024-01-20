from aiogram.utils.keyboard import InlineKeyboardBuilder

from Utils.classes import CallbackClasses


class AdminMenu:
    @staticmethod
    async def get_main_menu(
            user_id: int
    ) -> InlineKeyboardBuilder:
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text="Global Message", callback_data=CallbackClasses.AdminPanel.GlobalMessage(
            user_id=user_id
        ))
        return keyboard
