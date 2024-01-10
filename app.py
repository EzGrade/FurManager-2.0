import asyncio

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import Handlers
from Utils.Forms import CreatePost, EditDelay, EditChannels
from Utils.Functions import Text
from Utils.classes import CallbackClasses
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


@dp.message(StateFilter(EditDelay.waiting_for_post_delay))
async def post_delay_submit_handler(message: Message, state: FSMContext):
    await Handlers.post_delay_submit_handler(message, state)


@dp.message(StateFilter(CallbackClasses.AddChannelDoneCallback))
async def add_channel_done_handler(message: Message, state: FSMContext):
    await Handlers.channel_handler(message, state)


@dp.message(StateFilter(EditChannels.waiting_for_channel_name))
async def channel_name_handler(message: Message, state: FSMContext):
    await Handlers.channel_handler(message, state)


@dp.message()
async def handle_markup(message: Message, state: FSMContext):
    await Handlers.handle_markup(message, state)


@dp.callback_query(StateFilter(CreatePost.waiting_for_submit))
async def callback_handler(query: Message, state: FSMContext):
    await Handlers.submit_handler(query, state)


@dp.callback_query(CallbackClasses.DelayCallback.filter())
async def post_delay_handler(message: Message, state: FSMContext):
    await Handlers.post_delay_handler(message, state)


@dp.callback_query(CallbackClasses.EditChannelsCallback.filter())
async def edit_channels_handler(message: Message):
    await Handlers.get_channels_list(message)


@dp.callback_query(CallbackClasses.SettingsMenuCallback.filter())
async def settings_menu_handler(query: CallbackQuery):
    await Handlers.settings_handler(query)


@dp.callback_query(CallbackClasses.AddChannelCallback.filter())
async def add_channel_handler(query: CallbackQuery):
    await Handlers.add_bot_as_admin(query)


@dp.callback_query(CallbackClasses.CancelCallback.filter())
async def cancel_callback_handler(query: CallbackQuery, state: FSMContext):
    await Handlers.cancel_handler(query, state)


@dp.callback_query(CallbackClasses.AddChannelDoneCallback.filter())
async def add_channel_done_handler(query: CallbackQuery, state: FSMContext):
    await Handlers.add_bot_as_admin_process(query, state)


@dp.callback_query(CallbackClasses.RemoveChannelCallback.filter())
async def remove_channel_handler(query: CallbackQuery):
    await Handlers.remove_channel_handler(query, page=1)


@dp.callback_query(CallbackClasses.RemovePageCallback.filter())
async def page_handler(query: CallbackQuery, state: FSMContext):
    page = int(query.data.split(":")[2])
    await Handlers.remove_channel_handler(query, page)


@dp.callback_query(CallbackClasses.RemoveChannelDoneCallback.filter())
async def remove_channel_done_handler(query: CallbackQuery):
    await Handlers.remove_channel_done_handler(query)


@dp.callback_query(CallbackClasses.AddAdminsCallback.filter())
async def add_admins_handler(query: CallbackQuery):
    await Handlers.add_admins_handler(query)


@dp.callback_query(CallbackClasses.AddAdminDoneCallback.filter())
async def add_admins_done_handler(query: CallbackQuery):
    await Handlers.add_admins_done_handler(query, page=1)


@dp.callback_query(CallbackClasses.AddAdminPageCallback.filter())
async def add_admins_page_handler(query: CallbackQuery):
    page = int(query.data.split(":")[2])
    await Handlers.add_admins_done_handler(query, page)


@dp.callback_query(CallbackClasses.GetChannelRequestLink.filter())
async def get_channel_request_link_handler(query: CallbackQuery):
    await Handlers.get_channel_request_link_handler(query)


if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))
