from datetime import datetime, UTC

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, KeyboardButton, KeyboardButtonRequestChat
from aiogram.utils.keyboard import KeyboardBuilder

from Markup.settings_markup import AddChannelMenu, RemoveChannelMenu, EditChannelMenu
from Utils import forms
from Utils.functions import Channel, User, Text
from loader import bot


async def get_channels_list(query: CallbackQuery):
    channels_text = await Text.get_add_channel_text(query.from_user.id)
    await query.message.edit_text(channels_text,
                                  reply_markup=AddChannelMenu.add_channel_menu(query.from_user.id).as_markup())


async def add_bot_as_admin(query: CallbackQuery, state: FSMContext):
    keyboard = KeyboardBuilder(KeyboardButton)
    keyboard.button(text="➕Share channel",
                    request_chat=KeyboardButtonRequestChat(request_id=query.message.message_id, chat_is_channel=True))
    await query.message.delete()
    await query.message.answer(text="Share your channel", reply_markup=keyboard.as_markup())
    await state.set_state(forms.EditChannels.waiting_for_channel_name)


async def channel_handler(message: Message, state: FSMContext):
    channel_id = message.chat_shared.chat_id
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=bot.id)
        if member.status != "administrator":
            channels_text = await Text.get_add_channel_text(message.from_user.id)
            await message.answer(
                f"❌Please add the bot to the channel as an administrator and try again.\n{channels_text}",
                reply_markup=AddChannelMenu.add_channel_menu(message.from_user.id).as_markup())
        else:
            user_obj = await User.get_user(message.from_user.id)
            chat = await bot.get_chat(chat_id=channel_id)
            channels = user_obj.channel_id
            if channel_id not in channels:
                channels.append(channel_id)
            user_data = {
                "channel_id": user_obj.channel_id + [chat.id]
            }
            time_now = datetime.now(UTC)
            data = {
                "channel_id": chat.id,
                "channel_name": chat.title,
                "channel_holder": user_obj.pk,
                "channel_admins": [message.from_user.id],
                "delay_point": time_now,
            }
            result = await Channel.create_channel(data)
            channels_text = await Text.get_add_channel_text(message.from_user.id)
            if not isinstance(result, dict) and result is not False:
                await message.answer(
                    f"✅Well done! Bot added to your list of channels.\n{channels_text}",
                    reply_markup=AddChannelMenu.add_channel_menu(message.from_user.id).as_markup())
            elif not result:
                await message.answer(f"❌Something went wrong. Please try again later\n{channels_text}",
                                     reply_markup=AddChannelMenu.add_channel_menu(message.from_user.id).as_markup())
            elif isinstance(result, dict) and result["message"] == "Channel already exists":
                await message.answer(
                    f"❌Channel already added to bot list of channels. Contact channel holder to get access to channel\n{channels_text}",
                    reply_markup=AddChannelMenu.add_channel_menu(message.from_user.id).as_markup())
            else:
                await message.answer(f"✅Channel already in your list of channels\n{channels_text}",
                                     reply_markup=AddChannelMenu.add_channel_menu(message.from_user.id).as_markup())
    except TelegramBadRequest:
        channels_text = await Text.get_add_channel_text(message.from_user.id)
        await message.answer(
            f"❌The bot is not a member of this channel. Please add the bot to the channel and try again.\n{channels_text}",
            reply_markup=AddChannelMenu.add_channel_menu(message.from_user.id).as_markup())
    await state.clear()
    return


async def remove_channel_handler(query: CallbackQuery, page: int):
    keyboard = await RemoveChannelMenu.remove_channel_menu(
        user_id=query.from_user.id, page=page)
    await query.message.edit_text("👉Choose channel to remove", reply_markup=keyboard.as_markup())


async def remove_channel_done_handler(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    result = await Channel.delete_channel_by_id(channel_id)
    channels_text = await Text.get_add_channel_text(user_id)
    if result:
        await query.message.edit_text(f"✅Channel removed from list\n{channels_text}",
                                      reply_markup=AddChannelMenu.add_channel_menu(user_id).as_markup())
    else:
        await query.message.edit_text(f"❌Something went wrong. Please try again later\n{channels_text}",
                                      reply_markup=AddChannelMenu.add_channel_menu(user_id).as_markup())


async def edit_channel_page_handler(query: CallbackQuery, page: int):
    keyboard = await EditChannelMenu.get_edit_channel_menu(
        user_id=query.from_user.id, page=page)
    await query.message.edit_text("👉Choose channel to edit", reply_markup=keyboard.as_markup())
