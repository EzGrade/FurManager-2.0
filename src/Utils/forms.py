from aiogram.fsm.state import State, StatesGroup


class CreatePost(StatesGroup):
    waiting_for_photo = State()
    waiting_for_text = State()
    waiting_for_submit = State()


class EditChannels(StatesGroup):
    waiting_for_channel_name = State()
    waiting_for_template = State()


class AdminPanel(StatesGroup):
    waiting_for_code = State()

