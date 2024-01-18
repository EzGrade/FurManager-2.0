from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# DEV TOKEN 6645077129:AAFft23JjxYv727__oOgeiSim1vsSjMsoLM
# PROD TOKEN 6955659259:AAFrkK1TrJQSSMhLUy1O2xcEU-DUAJlLeJo

TOKEN = '6645077129:AAFft23JjxYv727__oOgeiSim1vsSjMsoLM'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
