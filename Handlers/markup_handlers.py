from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from Handlers.my_post_handlers import my_posts_main
from Markup.settings_markup import SettingsMenu
from Utils import functions
from Utils.forms import CreatePost


async def handle_markup(message: Message, state: FSMContext):
    if message.text == "➕Create post":
        channels = await functions.Channel.get_channels_by_user_id(message.from_user.id)
        if channels:
            await message.answer("⏳Send me a photo")
            await state.set_state(CreatePost.waiting_for_photo)
        else:
            await message.answer("❗️You don't have any channels. Create one first",
                                 reply_markup=SettingsMenu.get_settings_menu(message.from_user.id).as_markup())
    elif message.text == "📋My posts":
        await my_posts_main(message)
    elif message.text == "⚙️Settings":
        settings_text = await functions.Text.get_settings_text(message.from_user.id)
        await message.answer(settings_text,
                             reply_markup=SettingsMenu.get_settings_menu(message.from_user.id).as_markup())
