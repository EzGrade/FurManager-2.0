from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Markup.main_markup import get_main_menu
from Markup.settings_markup import SettingsMenu
from Utils import functions


async def start_handler(message: Message):
    data = {
        "user_id": message.from_user.id,
        "user_name": message.from_user.username if message.from_user.username is not None else "Unknown",
        "post_delay": 1
    }
    result = await functions.User.create_user(data)
    if result:
        await message.answer("Hello! I'm here to help you with posting in your Telegram channel",
                             reply_markup=get_main_menu().as_markup())
    else:
        await message.answer("Welcome back", reply_markup=get_main_menu().as_markup())


async def help_handler(message: Message):
    await message.answer("Send me pictures and I will post them in your channel")


async def settings_handler(message: Message):
    settings_text = await functions.Text.get_settings_text(message.from_user.id)
    if isinstance(message, Message):
        await message.answer(settings_text,
                             reply_markup=SettingsMenu.get_settings_menu(message.from_user.id).as_markup())
    elif isinstance(message, CallbackQuery):
        await message.message.edit_text(settings_text,
                                        reply_markup=SettingsMenu.get_settings_menu(message.from_user.id).as_markup())


async def cancel_handler(message: Message, state: FSMContext):
    await message.answer("Canceled")
    await state.clear()
