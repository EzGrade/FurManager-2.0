from aiogram.fsm.state import State, StatesGroup


class CreatePost(StatesGroup):
    waiting_for_photo = State()
    waiting_for_text = State()
    waiting_for_author = State()
    waiting_for_tags = State()
    waiting_for_submit = State()


class EditChannels(StatesGroup):
    waiting_for_channel_name = State()


class AdminPanel(StatesGroup):
    waiting_for_code = State()

