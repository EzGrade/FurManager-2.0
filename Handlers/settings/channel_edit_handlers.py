from datetime import datetime, UTC

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from Markup.settings_markup import EditSingleChannelMenu
from Utils import forms
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
    keyboard = await EditSingleChannelMenu.get_delay_main_menu(user_id, channel_id)
    text = await Text.get_delay_text(channel_id=channel_id)
    try:
        if result:
            await query.message.edit_text(text=f"{text}\n✅Success", reply_markup=keyboard.as_markup())
            return
        else:
            await query.message.edit_text(text=f"{text}\n❌Error", reply_markup=keyboard.as_markup())
            return
    except TelegramBadRequest:
        await query.answer()
        return


async def edit_delay_menu_handler(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    keyboard = await EditSingleChannelMenu.get_delay_main_menu(user_id, channel_id)
    text = await Text.get_delay_text(channel_id=channel_id)
    await query.message.edit_text(text=f"{text}", reply_markup=keyboard.as_markup())
    return


async def set_0_start_point(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    current_time = datetime.now(UTC)
    current_00 = datetime(year=current_time.year, month=current_time.month, day=current_time.day - 1, hour=18, minute=0)
    data = {
        "delay_point": current_00,
        "last_post": None
    }
    result = await Channel.update_channel(channel_id=channel_id, channel_data=data)
    keyboard = await EditSingleChannelMenu.get_delay_main_menu(user_id, channel_id)
    text = await Text.get_delay_text(channel_id=channel_id)
    try:
        if result:
            await query.message.edit_text(text=f"{text}\n✅Success", reply_markup=keyboard.as_markup())
            return
        else:
            await query.message.edit_text(text=f"{text}\n❌Error", reply_markup=keyboard.as_markup())
            return
    except TelegramBadRequest:
        await query.answer()
        return


async def edit_template_handler(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    keyboard = await EditSingleChannelMenu.get_template_menu(user_id, channel_id)
    text = await Text.template_text(channel_id=channel_id)
    await query.message.edit_text(text=f"{text}", reply_markup=keyboard.as_markup(), parse_mode="Markdown")
    return


async def ask_for_template_text(query: CallbackQuery, state: FSMContext):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    await state.update_data(user_id=user_id)
    await state.update_data(channel_id=channel_id)
    await query.message.edit_text(text="✏️Send me your template text", reply_markup=None)
    await state.set_state(forms.EditChannels.waiting_for_template)


async def process_template_text(message: Message, state: FSMContext):
    state_data = await state.get_data()
    user_id = state_data.get("user_id")
    channel_id = state_data.get("channel_id")
    text = message.text
    warnings_text = Text.process_template(text=text)
    if warnings_text:
        warnings_text = "\n".join([f"❗%{warning}%" for warning in warnings_text])
        warnings_text = f"\n⚠️Warnings\n{warnings_text}\n\nℹ️ Tags from warnings wont affect your caption"
    data = {
        "caption_template": text
    }
    result = await Channel.update_channel(channel_id=channel_id, channel_data=data)
    keyboard = await EditSingleChannelMenu.get_template_menu(user_id, channel_id)
    text = await Text.template_text(channel_id=channel_id)
    if warnings_text:
        text = f"{text}\n{warnings_text}"
    if result:
        await message.answer(text=f"{text}\n\n✅Success", reply_markup=keyboard.as_markup(), parse_mode="Markdown")
    else:
        await message.answer(text=f"{text}\n\n❌Error", reply_markup=keyboard.as_markup(), parse_mode="Markdown")
    await state.clear()
    return


async def edit_posts_number_menu_handler(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    keyboard = await EditSingleChannelMenu.get_posts_number_menu(user_id, channel_id)
    text = await Text.get_posts_number_text(channel_id=channel_id)
    await query.message.edit_text(text=f"{text}", reply_markup=keyboard.as_markup())
    return


async def edit_posts_number_value_handler(query: CallbackQuery):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    posts_number = int(query.data.split(":")[3])
    if posts_number < 1 or posts_number > 10:
        try:
            keyboard = await EditSingleChannelMenu.get_posts_number_menu(user_id, channel_id)
            await query.message.edit_text(
                text="❌Posts number cannot be smaller than 1 and bigger than 10\n",
                reply_markup=keyboard.as_markup())
            return
        except TelegramBadRequest:
            await query.answer()
            return
    data = {
        "posts_number": posts_number
    }
    result = await Channel.update_channel(channel_id=channel_id, channel_data=data)
    keyboard = await EditSingleChannelMenu.get_posts_number_menu(user_id, channel_id)
    text = await Text.get_posts_number_text(channel_id=channel_id)
    if result:
        await query.message.edit_text(text=f"{text}\n\n✅Success", reply_markup=keyboard.as_markup())
    else:
        await query.message.edit_text(text=f"{text}\n\n❌Error", reply_markup=keyboard.as_markup())


async def edit_enhance_links_handler(query: CallbackQuery, state: FSMContext):
    user_id = int(query.data.split(":")[1])
    channel_id = int(query.data.split(":")[2])
    channel_obj = await Channel.get_channel(channel_id=channel_id)
    data = {
        "enhance_links": not channel_obj.enhance_links
    }
    result = await Channel.update_channel(channel_id=channel_id, channel_data=data)
    keyboard = await EditSingleChannelMenu.get_main_menu(user_id=user_id, channel_id=channel_id)
    text = await Text.get_channel_settings_text(channel_id=channel_id)
    if result:
        await query.message.edit_text(text=f"{text}\n\n✅Success", reply_markup=keyboard.as_markup())
    else:
        await query.message.edit_text(text=f"{text}\n\n❌Error", reply_markup=keyboard.as_markup())
    return
