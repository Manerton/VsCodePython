import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram import types 
from config import TELEGRAM_TOKEN

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command_handler(message: types.Message):
    await bot.send_message(message.chat.id, "Вас приветсвует ваш личный Секретарь")
    
@dp.message(Command("category"))
async def display_all_category(message: types.Message):
    pass
    
    

# async def main() -> None:
#     # Initialize Bot instance with a default parse mode which will be passed to all API calls
#     # And the run events dispatching
#     await dp.start_polling(bot)
