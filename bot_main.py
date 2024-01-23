import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from config import TELEGRAM_TOKEN
from aiogram.utils.keyboard import InlineKeyboardBuilder
from controllers import category_contoller, note_contoller
from create_bot import bot, dp

dp.include_routers(category_contoller.router)
dp.include_routers(note_contoller.router)

@dp.message(Command("start"))
async def start_command_handler(message: types.Message):
    await bot.send_message(message.chat.id, "Вас приветсвует ваш личный Секретарь")
    
@dp.message(Command("menu"))
async def start_command_handler(message: types.Message):
    builder = InlineKeyboardBuilder()
    btn = types.InlineKeyboardButton(text="Показать список категорий", callback_data="categories")
    builder.add(btn)
    await bot.send_message(message.chat.id, "Меню:", reply_markup=builder.as_markup())
