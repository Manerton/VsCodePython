from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
from bot import bot, dp


async def lifespan(app: FastAPI):
    pass


async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)


app = FastAPI(lifespan=lifespan)


