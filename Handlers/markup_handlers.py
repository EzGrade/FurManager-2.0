from aiogram.types import Message
from aiogram.fsm.context import FSMContext


from Utils.forms import CreatePost


async def handle_markup(message: Message, state: FSMContext):
    if message.text == "➕Create post":
        await message.answer("⏳Send me a photo")
        await state.set_state(CreatePost.waiting_for_photo)
