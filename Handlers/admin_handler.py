from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Markup.admin_markup import AdminMenu
from Utils.forms import AdminPanel
from Utils.functions import Text, User
from loader import admins


async def admin_handler(message: Message):
    if message.from_user.id in admins:
        text = await Text.admin_panel_text()
        keyboard = await AdminMenu.get_main_menu(user_id=message.from_user.id)
        await message.answer(text=text, reply_markup=keyboard.as_markup())


async def global_message_handler(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text="Send me message to send to all users")
    await query.message.delete_reply_markup()
    await query.answer()
    await query.message.delete()
    await state.set_state(AdminPanel.waiting_for_global)


async def send_global_message_handler(message: Message, state: FSMContext):
    if message.from_user.id in admins:
        users = await User.get_all_user_ids()
        for user in users:
            try:
                await message.bot.send_message(chat_id=user, text=message.text)
            except Exception as e:
                print(e)
