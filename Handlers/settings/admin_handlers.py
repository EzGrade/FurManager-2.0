from urllib.parse import quote

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from Markup.settings_markup import AdminMenu
from Utils import forms
from Utils.functions import Channel, User
from loader import bot


async def add_admins_handler(query: CallbackQuery):
    await query.message.edit_text("☰Admin panel", reply_markup=AdminMenu.get_admin_menu(query.from_user.id).as_markup())


async def add_admins_done_handler(query: CallbackQuery, page: int):
    keyboard = await AdminMenu.get_add_admin_menu(query.from_user.id, page=page)
    await query.message.edit_text("👉Choose channel",
                                  reply_markup=keyboard.as_markup())


async def get_channel_request_link_handler(query: CallbackQuery):
    channel_id = int(query.data.split(":")[2])
    channel_code = await Channel.get_channel_request_code(channel_id)
    await query.message.edit_text(
        f"Send ```{quote(channel_code)}```to your channel's admin to get access to the bot"
        f"\nThis code will work only once, also you must accept request from admin",
        reply_markup=AdminMenu.get_admin_menu(query.from_user.id).as_markup(),
        parse_mode="Markdown")


async def admin_enter_link_handler(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text("⌨️Enter link")
    await state.set_state(forms.AdminPanel.waiting_for_code)


async def admin_handle_entered_code(message: Message, state: FSMContext):
    code = message.text
    channel = await Channel.get_channel_by_request_code(code)
    if not channel:
        await message.answer(text="❌Channel not found",
                             reply_markup=AdminMenu.get_admin_menu(message.from_user.id).as_markup())
        return
    channel_holder = await User.get_user_by_channel(channel)
    if channel_holder.user_id == message.from_user.id:
        await message.answer(text="❌You can't get access to your own channel",
                             reply_markup=AdminMenu.get_admin_menu(message.from_user.id).as_markup())
        return
    if channel:
        if message.from_user.username is not None:
            text = f"⏳@{message.from_user.username} wants to get access to your channel"
        else:
            text = f"⏳Unknown({message.from_user.id}) wants to get access to your channel"
        await message.answer(text="⏳Channel found, wait for its holder to accept your request")
        await bot.send_message(chat_id=channel_holder.user_id,
                               text=f"⏳User {message.from_user.id} wants to get access to your channel",
                               reply_markup=AdminMenu.accept_new_admin(user_id=message.from_user.id,
                                                                       channel_id=channel.channel_id).as_markup())
    else:
        await message.answer(text="❌Channel not found")


async def admin_accept_request_handler(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    user_obj = await User.get_user(user_id)
    channel = await Channel.get_channel(channel_id)
    holder = await User.get_user_by_channel(channel)
    if channel_id not in user_obj.channel_id and holder.user_id != user_id:
        await Channel.add_admin(user_id, channel_id)
        data = {
            "channel_id": user_obj.channel_id + [channel_id]
        }
        await User.update_user(user_id=user_id, user_data=data)
    await Channel.update_request_code(channel_id)
    await query.message.edit_text("✅Request accepted")
    await bot.send_message(chat_id=user_id, text="✅Your request was accepted")


async def admin_remove_markup_handler(query: CallbackQuery):
    keyboard = await AdminMenu.get_remove_admin_menu(query.from_user.id, page=1)
    await query.message.edit_text("👉Choose channel to remove admin from",
                                  reply_markup=keyboard.as_markup())


async def admin_remove_handler(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    keyboard = await AdminMenu.admins_to_remove_menu(user_id, channel_id, page=1)
    await query.message.edit_text("👉Choose admin to remove", reply_markup=keyboard.as_markup())


async def admin_remove_admin_page_handler(query: CallbackQuery, page: int):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    keyboard = await AdminMenu.admins_to_remove_menu(user_id, channel_id, page=page)
    await query.message.edit_text("👉Choose admin to remove", reply_markup=keyboard.as_markup())


async def admin_channel_remove_admin_page_handler(query: CallbackQuery, page: int):
    user_id = int(query.data.split(":")[1])
    keyboard = await AdminMenu.get_remove_admin_menu(user_id, page=page)
    await query.message.edit_text("👉Choose admin to remove", reply_markup=keyboard.as_markup())


async def admin_remove_admin_done_handler(query: CallbackQuery):
    data = query.data.split(":")
    user_id = int(data[1])
    channel_id = int(data[2])
    admin_id = int(data[3])
    result = await Channel.remove_admin(user_id=user_id, channel_id=channel_id, admin_id=admin_id)
    keyboard = AdminMenu.get_admin_menu(user_id)
    if result:
        await query.message.edit_text("✅Admin removed", reply_markup=keyboard.as_markup())
    else:
        await query.message.edit_text("❌Admin not found", reply_markup=keyboard.as_markup())
