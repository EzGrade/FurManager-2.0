from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from Markup.settings_markup import EditSingleChannelMenu
from Utils.functions import Channel


async def edit_main_menu(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    keyboard = await EditSingleChannelMenu.get_main_menu(user_id, channel_id)
    await query.message.edit_text(text="Channel Editing Menu", reply_markup=keyboard.as_markup())
    return


async def edit_channel_delay_handler(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    keyboard = await EditSingleChannelMenu.get_delay_menu(user_id, channel_id)
    await query.message.edit_text(text="Delay edit menu", reply_markup=keyboard.as_markup())
    return


async def edit_channel_delay_value_handler(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    delay = int(query.data.split(":")[3])
    if delay < 5 or delay > 180:
        try:
            keyboard = await EditSingleChannelMenu.get_delay_menu(user_id, channel_id)
            await query.message.edit_text(text="❌Delay value cannot be smaller than 5 and bigger than 180\nDelay edit menu",
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
        await query.message.edit_text(text="Delay edit menu", reply_markup=keyboard.as_markup())
    else:
        try:
            keyboard = await EditSingleChannelMenu.get_delay_menu(user_id, channel_id)
            await query.message.edit_text(text="❌Error\nDelay edit menu", reply_markup=keyboard.as_markup())
        except TelegramBadRequest:
            await query.answer()
            return
