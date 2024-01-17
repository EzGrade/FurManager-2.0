from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

TOKEN = '6955659259:AAFrkK1TrJQSSMhLUy1O2xcEU-DUAJlLeJo'
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)
