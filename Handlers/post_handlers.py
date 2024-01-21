from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Markup.post_menu import PostMenu
from Utils import functions
from Utils.forms import CreatePost
from loader import bot


async def photo_handler(message: Message, state: FSMContext):
    if message.photo is not None:
        await state.update_data(photo=message.photo[-1].file_id)
        await state.update_data(type="photo")
    elif message.animation is not None:
        await state.update_data(animation=message.animation.file_id)
        await state.update_data(type="gif")
    elif message.video is not None:
        await state.update_data(video=message.video.file_id)
        await state.update_data(type="video")
    await message.answer("⌨️Send me caption for your post or . to skip it")
    await state.set_state(CreatePost.waiting_for_text)


async def finish_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    caption_to_db = message.text.replace(".", "\.") if message.text != "." else ""
    caption = message.text if message.text != "." else ""
    await state.update_data(caption=caption_to_db)
    keyboard = await PostMenu.get_channels_menu(user_id=message.from_user.id, checked_channels_list=[])
    if data["type"] == "photo":
        await message.answer_photo(photo=data["photo"], caption=caption,
                                   reply_markup=keyboard.as_markup())
    elif data["type"] == "gif":
        await message.answer_animation(animation=data["animation"], caption=caption, reply_markup=keyboard.as_markup())
    elif data["type"] == "video":
        await message.answer_video(video=data["video"], caption=caption, reply_markup=keyboard.as_markup())


async def change_list_of_channels(query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    query_data = query.data
    user_id = query_data.split(":")[1]
    channel_id = query_data.split(":")[2]
    page = int(query_data.split(":")[3])
    try:
        checked_channels_list = state_data["checked_channels_list"]
    except KeyError:
        checked_channels_list = []
    if channel_id in checked_channels_list:
        checked_channels_list.remove(channel_id)
    else:
        checked_channels_list.append(channel_id)
    await state.update_data(checked_channels_list=checked_channels_list)
    keyboard = await PostMenu.get_channels_menu(user_id=user_id, checked_channels_list=checked_channels_list, page=page)
    await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())


async def channels_menu_callback_handler(query: CallbackQuery, state: FSMContext):
    query_data = query.data
    state_data = await state.get_data()
    user_id = query_data.split(":")[1]
    page = int(query_data.split(":")[2])
    try:
        checked_channels_list = state_data["checked_channels_list"]
    except KeyError:
        checked_channels_list = []
    keyboard = await PostMenu.get_channels_menu(user_id=user_id, checked_channels_list=checked_channels_list, page=page)
    await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())


async def post_to_queue_callback_handler(query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    channels = []
    for channel_id in state_data["checked_channels_list"]:
        channel_obj = await functions.Channel.get_channel(channel_id)
        channels.append(channel_obj.pk)
    media_type = state_data["type"]
    if media_type == "photo":
        media = state_data["photo"]
    elif media_type == "gif":
        media = state_data["animation"]
    elif media_type == "video":
        media = state_data["video"]
    post_data = {
        "photo": media,
        "media_type": media_type,
        "caption": state_data["caption"] if state_data["caption"] else None,
    }
    post = await functions.Post.create_post(post_data)
    result = await functions.Post.set_channels(post.pk, channels)
    if result:
        await query.message.answer(text="✅Successfully added to queue")
    else:
        await query.message.answer(text="❌Error adding to queue")
    await query.answer()
    await query.message.delete()
    await state.clear()


async def post_now_callback_handler(query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    user_id = query.data.split(":")[1]
    try:
        checked_channels_list = state_data["checked_channels_list"]
    except KeyError:
        checked_channels_list = []
    media_type = state_data["type"]
    if media_type == "photo":
        media = state_data["photo"]
    elif media_type == "gif":
        media = state_data["animation"]
    elif media_type == "video":
        media = state_data["video"]
    json_data = {
        "photo": media,
        "media_type": media_type,
        "caption": state_data["caption"] if state_data["caption"] else None,
        "channels": checked_channels_list
    }
    not_success = []
    await query.message.answer(text="⏳Posting...")
    for post_object in json_data["channels"]:
        channel_obj = await functions.Channel.get_channel(post_object)
        try:
            caption = await functions.Text.format_caption(json_data["caption"], channel_obj.channel_id)
            if json_data["media_type"] == "photo":
                await bot.send_photo(chat_id=channel_obj.channel_id, photo=json_data["photo"], caption=caption,
                                     parse_mode="MarkdownV2")
            elif json_data["media_type"] == "gif":
                await bot.send_animation(chat_id=channel_obj.channel_id, animation=json_data["photo"], caption=caption,
                                         parse_mode="MarkdownV2")
            elif json_data["media_type"] == "video":
                await bot.send_video(chat_id=channel_obj.channel_id, video=json_data["photo"], caption=caption,
                                     parse_mode="MarkdownV2")
            await query.message.answer(text=f"✅Successfully posted in {channel_obj.channel_name}")
        except Exception as e:
            print(e)
            not_success += [channel_obj.channel_name]
    if len(not_success) == 0:
        await query.message.answer(text="✅Successfully posted in all channels")
    else:
        await query.message.answer(text=f"❌Error posting in {', '.join(not_success)}")
        await query.answer()
    await query.message.delete()
    await state.clear()


async def select_all_handler(query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    user_id = query.data.split(":")[1]
    page = int(query.data.split(":")[2])
    try:
        checked_channels_list = state_data["checked_channels_list"]
    except KeyError:
        checked_channels_list = []
    user_obj = await functions.User.get_user(user_id)
    channels_list = user_obj.channel_id
    if user_obj.channel_id != list(map(int, checked_channels_list)):
        checked_channels_list = list(map(str, channels_list))
    else:
        checked_channels_list = []
    await state.update_data(checked_channels_list=checked_channels_list)
    keyboard = await PostMenu.get_channels_menu(user_id=user_id, checked_channels_list=checked_channels_list, page=page)
    await query.message.edit_reply_markup(reply_markup=keyboard.as_markup())
