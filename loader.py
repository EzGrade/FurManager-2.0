from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

TOKENS = {
    "DEV": "6645077129:AAFft23JjxYv727__oOgeiSim1vsSjMsoLM",
    "PROD": "6955659259:AAFrkK1TrJQSSMhLUy1O2xcEU-DUAJlLeJo"
}

DEV = True

if DEV:
    TOKEN = TOKENS["DEV"]
else:
    TOKEN = TOKENS["PROD"]

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
