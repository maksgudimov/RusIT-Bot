from aiogram import Bot,types,Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from starlette.config import Config
import logging

config = Config('.env')

bot = Bot(config("TOKEN"))
dp = Dispatcher(bot,storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)