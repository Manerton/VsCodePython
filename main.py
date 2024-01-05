from fastapi import FastAPI
from aiogram import types
from create_bot import bot, dp
from database.db import create_main_tables
from config import TELEGRAM_TOKEN, NGROK_TUNNEL_URL
import bot_main


WEBHOOK_PATH = f"/bot/{TELEGRAM_TOKEN}"
WEBHOOK_URL = f"{NGROK_TUNNEL_URL}{WEBHOOK_PATH}"


async def lifespan(app: FastAPI):
    webhook_info = await bot.get_webhook_info()
    create_main_tables()
    if webhook_info.url != WEBHOOK_URL:
        await bot.delete_webhook()
        await bot.set_webhook(url=WEBHOOK_URL)
    yield
    await bot.session.close()
    
app = FastAPI(lifespan=lifespan)

@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp._process_update(bot=bot, update=telegram_update)

