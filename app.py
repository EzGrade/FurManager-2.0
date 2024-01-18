import setup
import asyncio
import logging

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


@dp.message(F.text, StateFilter(CreatePost.waiting_for_text))
async def finish_handler(message: Message, state: FSMContext):
    await Handlers.finish_handler(message, state)


@dp.message(StateFilter(EditChannels.waiting_for_channel_name))
async def channel_name_handler(message: Message, state: FSMContext):
    await Handlers.channel_handler(message, state)


@dp.message(StateFilter(AdminPanel.waiting_for_code))
async def admin_enter_link_handler(message: Message, state: FSMContext):
    await Handlers.admin_handle_entered_code(message, state)


@dp.message(StateFilter(EditChannels.waiting_for_template))
async def template_handler(message: Message, state: FSMContext):
    await Handlers.process_template_text(message, state)


@dp.message()
async def handle_markup(message: Message, state: FSMContext):
    await Handlers.handle_markup(message, state)


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


@dp.callback_query(CallbackClasses.QuitCallback.filter())
async def quit_callback_handler(query: CallbackQuery, state: FSMContext):
    await Handlers.quit_callback_handler(query, state)


@dp.callback_query(CallbackClasses.PostCallbacks.ChooseChannelCallback.filter())
async def choose_channel_callback_handler(query: CallbackQuery, state: FSMContext):
    await Handlers.change_list_of_channels(query, state)


@dp.callback_query(CallbackClasses.PostCallbacks.ChannelsMenuCallback.filter())
async def channels_menu_callback_handler(query: CallbackQuery, state: FSMContext):
    await Handlers.channels_menu_callback_handler(query, state)


@dp.callback_query(CallbackClasses.PostCallbacks.PostToQueue.filter())
async def post_to_queue_callback_handler(query: CallbackQuery, state: FSMContext):
    await Handlers.post_to_queue_callback_handler(query, state)


@dp.callback_query(CallbackClasses.PostCallbacks.PostNow.filter())
async def post_now_callback_handler(query: CallbackQuery, state: FSMContext):
    await Handlers.post_now_callback_handler(query, state)


@dp.callback_query(CallbackClasses.PostCallbacks.SelectAll.filter())
async def select_all_callback_handler(query: CallbackQuery, state: FSMContext):
    await Handlers.select_all_handler(query, state)


@dp.callback_query(CallbackClasses.EditSingleChannelCallbacks.EditChannelActiveCallback.filter())
async def edit_channel_active_state_handler(query: CallbackQuery):
    await Handlers.edit_channel_active_sate(query)


@dp.callback_query(CallbackClasses.EditSingleChannelCallbacks.EditDelayStartPoint.filter())
async def edit_delay_start_point_handler(query: CallbackQuery):
    await Handlers.edit_delay_start_point_handler(query)


@dp.callback_query(CallbackClasses.MyPosts.MyPostsMenu.filter())
async def my_posts_menu_handler(query: CallbackQuery):
    await Handlers.my_posts_main(query)


@dp.callback_query(CallbackClasses.MyPosts.DeletePost.filter())
async def delete_post_handler(query: CallbackQuery):
    await Handlers.delete_post_handler(query)


@dp.callback_query(CallbackClasses.MyPosts.PostNow.filter())
async def post_now_handler(query: CallbackQuery):
    await Handlers.post_now_handler(query)


@dp.callback_query(CallbackClasses.MyPosts.EditChannels.filter())
async def edit_channels_handler(query: CallbackQuery):
    await Handlers.edit_channels_handler(query)


@dp.callback_query(CallbackClasses.MyPosts.AddChannelToPost.filter())
async def update_post_channels_handler(query: CallbackQuery):
    await Handlers.add_channel_to_post(query)


@dp.callback_query(CallbackClasses.MyPosts.RemoveChannelFromPost.filter())
async def update_post_channels_handler(query: CallbackQuery):
    await Handlers.remove_channel_from_post(query)


@dp.callback_query(CallbackClasses.MyPosts.BackToMain.filter())
async def my_posts_back_to_main_handler(query: CallbackQuery):
    await Handlers.my_posts_main_back(query)


@dp.callback_query(CallbackClasses.EditSingleChannelCallbacks.EditDelayMenu.filter())
async def edit_delay_menu_handler(query: CallbackQuery):
    await Handlers.edit_delay_menu_handler(query)


@dp.callback_query(CallbackClasses.EditSingleChannelCallbacks.SetDelay00.filter())
async def set_delay_00_handler(query: CallbackQuery):
    await Handlers.set_0_start_point(query)


@dp.callback_query(CallbackClasses.EditSingleChannelCallbacks.EditTemplate.filter())
async def edit_template_handler(query: CallbackQuery):
    await Handlers.edit_template_handler(query)


@dp.callback_query(CallbackClasses.EditSingleChannelCallbacks.EditTemplateValue.filter())
async def edit_template_value_handler(query: CallbackQuery, state: FSMContext):
    await Handlers.ask_for_template_text(query, state)


@dp.callback_query(CallbackClasses.EditSingleChannelCallbacks.EditPostsNumberMenu.filter())
async def edit_posts_number_menu_handler(query: CallbackQuery):
    await Handlers.edit_posts_number_menu_handler(query)


@dp.callback_query(CallbackClasses.EditSingleChannelCallbacks.EditPostsNumberValue.filter())
async def edit_posts_number_value_handler(query: CallbackQuery):
    await Handlers.edit_posts_number_value_handler(query)


@dp.callback_query(CallbackClasses.EmptyCallback.filter())
async def empty_callback_handler(query: CallbackQuery):
    await query.answer()


async def run():
    print("Starting bot...")
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run())
