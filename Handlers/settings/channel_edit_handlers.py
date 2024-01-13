from datetime import datetime, UTC

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from Markup.settings_markup import EditSingleChannelMenu
from Utils.functions import Channel, Text


async def edit_main_menu(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    keyboard = await EditSingleChannelMenu.get_main_menu(user_id, channel_id)
    text = await Text.get_channel_settings_text(channel_id=channel_id)
    await query.message.edit_text(text=f"{text}", reply_markup=keyboard.as_markup())
    return


async def edit_channel_delay_handler(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    keyboard = await EditSingleChannelMenu.get_delay_menu(user_id, channel_id)
    await query.message.edit_text(text="⚙️Delay edit menu", reply_markup=keyboard.as_markup())
    return


async def edit_channel_delay_value_handler(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    delay = int(query.data.split(":")[3])
    if delay < 5 or delay > 180:
        try:
            keyboard = await EditSingleChannelMenu.get_delay_menu(user_id, channel_id)
            await query.message.edit_text(
                text="❌Delay value cannot be smaller than 5 and bigger than 180\n⚙️Delay edit menu",
                reply_markup=keyboard.as_markup())
            return
        except TelegramBadRequest:
            await query.answer()
            return
    data = {
        "channel_delay": delay,
    }
    result = await Channel.update_channel(channel_id=channel_id, channel_data=data)
    if result:
        keyboard = await EditSingleChannelMenu.get_delay_menu(user_id, channel_id)
        await query.message.edit_text(text="⚙️Delay edit menu", reply_markup=keyboard.as_markup())
    else:
        try:
            keyboard = await EditSingleChannelMenu.get_delay_menu(user_id, channel_id)
            await query.message.edit_text(text="❌Error\n⚙️Delay edit menu", reply_markup=keyboard.as_markup())
        except TelegramBadRequest:
            await query.answer()
            return


async def edit_channel_active_sate(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    channel_obj = await Channel.get_channel(channel_id)
    data = {
        "active": not channel_obj.active
    }
    result = await Channel.update_channel(channel_id=channel_id, channel_data=data)
    if result:
        keyboard = await EditSingleChannelMenu.get_main_menu(user_id=user_id, channel_id=channel_id)
        text = await Text.get_channel_settings_text(channel_id=channel_id)
        await query.message.edit_text(text=f"{text}", reply_markup=keyboard.as_markup())
    else:
        try:
            keyboard = await EditSingleChannelMenu.get_main_menu(user_id=channel_obj.channel_admin,
                                                                 channel_id=channel_id)
            text = await Text.get_channel_settings_text(channel_id=channel_id)
            await query.message.edit_text(text=f"❌Error\n{text}",
                                          reply_markup=keyboard.as_markup())
        except TelegramBadRequest:
            await query.answer()
            return


async def edit_delay_start_point_handler(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    date = datetime.now(UTC)
    data = {
        "delay_point": date,
        "last_post": None
    }
    result = await Channel.update_channel(channel_id=channel_id, channel_data=data)
    keyboard = await EditSingleChannelMenu.get_main_menu(user_id, channel_id)
    text = await Text.get_channel_settings_text(channel_id=channel_id)
    try:
        if result:
            await query.message.edit_text(text=f"{text}", reply_markup=keyboard.as_markup())
            return
        else:
            await query.message.edit_text(text=f"❌Error\n{text}", reply_markup=keyboard.as_markup())
            return
    except TelegramBadRequest:
        await query.answer()
        return
