# Импорт библиотек
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor  # Импортируем executor из aiogram
from config import TOKEN
import handlers

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

if __name__ == '__main__':
    handlers.register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)  # Используем корректный импорт
