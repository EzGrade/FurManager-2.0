from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from Markup.settings_markup import SettingsMenu
from Utils import Functions, Forms


async def post_delay_handler(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(text="Enter new post delay in minutes")
    await state.set_state(Forms.EditDelay.waiting_for_post_delay)


async def post_delay_submit_handler(message: Message, state: FSMContext):
    try:
        delay = int(message.text.split("_")[-1])
    except ValueError:
        settings_text = await Functions.Text.get_settings_text(user_id=message.from_user.id)
        await message.answer(text=f"⚠️Wrong input, try again\n{settings_text}",
                             reply_markup=SettingsMenu.get_settings_menu(
                                 message.from_user.id).as_markup())
        return
    data = {
        "post_delay": delay
    }
    result = await Functions.User.update_user(user_id=message.from_user.id, user_data=data)
    settings_text = await Functions.Text.get_settings_text(user_id=message.from_user.id)
    if not result:
        await message.answer(text=f"⚠️Something went wrong, try again\n{settings_text}",
                             reply_markup=SettingsMenu.get_settings_menu(
                                 message.from_user.id).as_markup())
    else:
        await message.answer(text=f"✅Posting delay successfully changed\n{settings_text}",
                             reply_markup=SettingsMenu.get_settings_menu(
                                 message.from_user.id).as_markup())
    await state.clear()
