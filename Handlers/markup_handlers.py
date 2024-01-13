from aiogram.types import Message
from aiogram.fsm.context import FSMContext


from Utils.forms import CreatePost
from Handlers.my_post_handlers import my_posts_main


async def handle_markup(message: Message, state: FSMContext):
    if message.text == "➕Create post":
        await message.answer("⏳Send me a photo")
        await state.set_state(CreatePost.waiting_for_photo)
    elif message.text == "📋My posts":
        await my_posts_main(message)