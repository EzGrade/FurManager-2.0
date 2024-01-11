import asyncio

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import Handlers
from Utils.classes import CallbackClasses
from Utils.forms import CreatePost, EditChannels, AdminPanel
from Utils.functions import Text
from loader import dp, bot


@dp.message(Text.is_text("/start"), StateFilter(None))
async def start_handler(message: Message):
    await Handlers.start_handler(message)


@dp.message(Text.is_text("/help"))
async def help_handler(message: Message):
    await Handlers.help_handler(message)


@dp.message(Text.is_text("/settings"))
async def settings_handler(message: Message):
    await Handlers.settings_handler(message)


@dp.message(Text.is_text("/cancel"))
async def cancel_handler(message: Message, state: FSMContext):
    await Handlers.cancel_handler(message, state)


@dp.message(F.photo, StateFilter(CreatePost.waiting_for_photo))
async def photo_handler(message: Message, state: FSMContext):
    await Handlers.photo_handler(message, state)


@dp.message(StateFilter(CreatePost.waiting_for_author))
async def author_handler(message: Message, state: FSMContext):
    await Handlers.author_handler(message, state)


@dp.message(StateFilter(CreatePost.waiting_for_tags))
async def tags_handler(message: Message, state: FSMContext):
    await Handlers.tags_handler(message, state)


@dp.message(StateFilter(EditChannels.waiting_for_channel_name))
async def channel_name_handler(message: Message, state: FSMContext):
    await Handlers.channel_handler(message, state)


@dp.message(StateFilter(AdminPanel.waiting_for_code))
async def admin_enter_link_handler(message: Message, state: FSMContext):
    await Handlers.admin_handle_entered_code(message, state)


@dp.message()
async def handle_markup(message: Message, state: FSMContext):
    await Handlers.handle_markup(message, state)


@dp.callback_query(StateFilter(CreatePost.waiting_for_submit))
async def callback_handler(query: Message, state: FSMContext):
    await Handlers.submit_handler(query, state)


@dp.callback_query(CallbackClasses.ChannelCallbacks.EditChannelsCallback.filter())
async def edit_channels_handler(message: Message):
    await Handlers.get_channels_list(message)


@dp.callback_query(CallbackClasses.SettingsCallbacks.SettingsMenuCallback.filter())
async def settings_menu_handler(query: CallbackQuery):
    await Handlers.settings_handler(query)


@dp.callback_query(CallbackClasses.ChannelCallbacks.AddChannelCallback.filter())
async def add_channel_handler(query: CallbackQuery):
    await Handlers.add_bot_as_admin(query)


@dp.callback_query(CallbackClasses.CommandCallbacks.CancelCallback.filter())
async def cancel_callback_handler(query: CallbackQuery, state: FSMContext):
    await Handlers.cancel_handler(query, state)


@dp.callback_query(CallbackClasses.AdminCallbacks.AdminRemoveAdmin.filter())
async def add_channel_done_handler(query: CallbackQuery, state: FSMContext):
    await Handlers.admin_remove_markup_handler(query)


@dp.callback_query(CallbackClasses.AdminCallbacks.ChannelRemoveAdmin.filter())
async def admins_to_remove_handler(query: CallbackQuery, state: FSMContext):
    await Handlers.admin_remove_handler(query)


@dp.callback_query(CallbackClasses.ChannelCallbacks.RemoveChannelCallback.filter())
async def remove_channel_handler(query: CallbackQuery):
    await Handlers.remove_channel_handler(query, page=1)


@dp.callback_query(CallbackClasses.ChannelCallbacks.RemovePageCallback.filter())
async def page_handler(query: CallbackQuery, state: FSMContext):
    page = int(query.data.split(":")[2])
    await Handlers.remove_channel_handler(query, page)


@dp.callback_query(CallbackClasses.ChannelCallbacks.RemoveChannelDoneCallback.filter())
async def remove_channel_done_handler(query: CallbackQuery):
    await Handlers.remove_channel_done_handler(query)


@dp.callback_query(CallbackClasses.AdminCallbacks.AddAdminsCallback.filter())
async def add_admins_handler(query: CallbackQuery):
    await Handlers.add_admins_handler(query)


@dp.callback_query(CallbackClasses.AdminCallbacks.AddAdminDoneCallback.filter())
async def add_admins_done_handler(query: CallbackQuery):
    await Handlers.add_admins_done_handler(query, page=1)


@dp.callback_query(CallbackClasses.AdminCallbacks.AddAdminPageCallback.filter())
async def add_admins_page_handler(query: CallbackQuery):
    page = int(query.data.split(":")[2])
    await Handlers.add_admins_done_handler(query, page)


@dp.callback_query(CallbackClasses.ChannelCallbacks.GetChannelRequestLink.filter())
async def get_channel_request_link_handler(query: CallbackQuery):
    await Handlers.get_channel_request_link_handler(query)


@dp.callback_query(CallbackClasses.AdminCallbacks.AdminEnterLinkCallback.filter())
async def admin_enter_link_handler(query: CallbackQuery, state: FSMContext):
    await Handlers.admin_enter_link_handler(query, state)


@dp.callback_query(CallbackClasses.AdminCallbacks.AdminAcceptRequest.filter())
async def admin_accept_request_handler(query: CallbackQuery):
    await Handlers.admin_accept_request_handler(query)


@dp.callback_query(CallbackClasses.ChannelCallbacks.EditChannelPageCallback.filter())
async def edit_channel_page_handler(query: CallbackQuery):
    page = int(query.data.split(":")[2])
    await Handlers.edit_channel_page_handler(query, page)


@dp.callback_query(CallbackClasses.AdminCallbacks.AdminRemoveAdminPage.filter())
async def admin_remove_admin_page_handler(query: CallbackQuery):
    page = int(query.data.split(":")[3])
    await Handlers.admin_remove_admin_page_handler(query, page)


@dp.callback_query(CallbackClasses.AdminCallbacks.AdminChannelRemoveAdminPage.filter())
async def admin_channel_remove_admin_page_handler(query: CallbackQuery):
    page = int(query.data.split(":")[2])
    await Handlers.admin_channel_remove_admin_page_handler(query, page)


@dp.callback_query(CallbackClasses.AdminCallbacks.AdminRemoveAdminDone.filter())
async def admin_remove_admin_done_handler(query: CallbackQuery):
    await Handlers.admin_remove_admin_done_handler(query)


@dp.callback_query(CallbackClasses.ChannelCallbacks.AddChannelDoneCallback.filter())
async def add_channel_done_handler(message: Message, state: FSMContext):
    await Handlers.wait_for_channel_name(message, state)


@dp.callback_query(CallbackClasses.ChannelCallbacks.EditChannelCallback.filter())
async def edit_channel_handler(query: CallbackQuery):
    await Handlers.edit_main_menu(query)


@dp.callback_query(CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayCallback.filter())
async def edit_channel_delay_handler(query: CallbackQuery):
    await Handlers.edit_channel_delay_handler(query)


@dp.callback_query(CallbackClasses.EditSingleChannelCallbacks.EditChannelDelayValue.filter())
async def edit_channel_delay_value_handler(query: CallbackQuery):
    await Handlers.edit_channel_delay_value_handler(query)

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
