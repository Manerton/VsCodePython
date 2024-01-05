import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from config import TELEGRAM_TOKEN
from controllers import category_contoller, note_contoller
from create_bot import bot, dp

dp.include_routers(category_contoller.router)
dp.include_routers(note_contoller.router)

@dp.message(Command("start"))
async def start_command_handler(message: types.Message):
    replay_key_buttons = [
        [types.KeyboardButton(text="/categories") ],
        [types.KeyboardButton(text="/create_category")]
    ]
    markup = types.ReplyKeyboardMarkup(keyboard=replay_key_buttons)
    await bot.send_message(message.chat.id, "Вас приветсвует ваш личный Секретарь", reply_markup=markup)
    


# async def main() -> None:
#     # Initialize Bot instance with a default parse mode which will be passed to all API calls
#     # And the run events dispatching
#     await dp.start_polling(bot)
