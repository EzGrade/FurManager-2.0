from urllib.parse import quote

from aiogram.types import CallbackQuery

from Markup.settings_markup import AdminMenu
from Utils.Functions import Channel


async def add_admins_handler(query: CallbackQuery):
    await query.message.edit_text("Admin panel", reply_markup=AdminMenu.get_admin_menu(query.from_user.id).as_markup())


async def add_admins_done_handler(query: CallbackQuery, page: int):
    keyboard = await AdminMenu.get_add_admin_menu(query.from_user.id, page=page)
    await query.message.edit_text("Choose channel",
                                  reply_markup=keyboard.as_markup())


async def get_channel_request_link_handler(query: CallbackQuery):
    channel_id = int(query.data.split(":")[2])
    channel_code = await Channel.get_channel_request_code(channel_id)
    await query.message.edit_text(
        f"Send ```{quote(channel_code)}```to your channel's admin to get access to the bot"
        f"\nThis code will work only once, also you must accept request from admin",
        reply_markup=AdminMenu.get_admin_menu(query.from_user.id).as_markup(),
        parse_mode="Markdown")
