from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .config import config

bot = Bot(token=config.bot_token, parse_mode="HTML")
dispatcher = Dispatcher(storage=MemoryStorage())
