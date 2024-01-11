from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from Markup import get_submit_menu
from Utils import functions
from Utils.forms import CreatePost


async def photo_handler(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer("Send me author for your post or . for not adding author")
    await state.set_state(CreatePost.waiting_for_author)


async def author_handler(message: Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(author="")
    else:
        await state.update_data(author=message.text)
    await message.answer("Send me tags for your post or . for not adding tags")
    await state.set_state(CreatePost.waiting_for_tags)


async def tags_handler(message: Message, state: FSMContext):
    if message.text == '.':
        tags = ""
    elif ',' in message.text:
        tags = message.text.split(',')
        tags = ["#" + i.strip() if "#" not in i.strip() else i.strip() for i in tags]
        tags = ' '.join(tags)
    elif ' ' in message.text:
        tags = message.text.split(' ')
        tags = ["#" + i.strip() if "#" not in i.strip() else i.strip() for i in tags]
        tags = ' '.join(tags)
    else:
        tags = "#" + message.text.strip() if "#" not in message.text.strip() else message.text.strip()

    await state.update_data(tags=tags)
    await finish_handler(message, state)


async def finish_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    author = "Author: " + data["author"] if data["author"] else ""
    tags = "Tags: " + data["tags"] if data["tags"] else ""
    caption = [author] if author else []
    caption += [tags] if tags else []
    if caption:
        caption = '\n'.join(caption)
    else:
        caption = ''
    await message.answer_photo(photo=data["photo"], caption=caption,
                               reply_markup=get_submit_menu().as_markup())
    await state.set_state(CreatePost.waiting_for_submit)


async def submit_handler(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_obj = await Functions.User.get_user(query.from_user.id)
    json_data = {
        "photo": data["photo"] if data["photo"] else None,
        "author": data["author"] if data["author"] else None,
        "tags": data["tags"] if data["tags"] else None,
        "user": user_obj.pk
    }
    result = await Functions.Post.create_post(json_data)
    await query.answer()
    await query.message.delete()
    if result:
        await query.message.answer(text="Successfully added to queue")
    else:
        await query.message.answer(text="Error, try again later")
