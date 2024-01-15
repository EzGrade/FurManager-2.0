from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


async def cancel_handler(message: Message, state: FSMContext):
    if isinstance(message, Message):
        await message.edit_text("❌Canceled")
        await state.clear()
    elif isinstance(message, CallbackQuery):
        await message.message.edit_text("❌Canceled")
        await state.clear()


async def quit_callback_handler(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer(text="❌Canceled")
    await state.clear()
