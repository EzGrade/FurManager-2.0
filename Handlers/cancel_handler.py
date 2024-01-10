from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


async def cancel_handler(message: Message, state: FSMContext):
    if isinstance(message, Message):
        await message.edit_text("Canceled")
        await state.clear()
    elif isinstance(message, CallbackQuery):
        await message.message.edit_text("Canceled")
        await state.clear()
