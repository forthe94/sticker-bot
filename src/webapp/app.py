from aiogram import types
from fastapi import FastAPI

from src import config
from src.bot.bot import dispatcher, requests_data, sticker_bot
from src.webapp.middleware import log_errors_to_tg

app = FastAPI()

app.middleware("HTTP")(log_errors_to_tg)


@app.on_event("startup")
async def on_startup():
    webhook_info = await sticker_bot.get_webhook_info()
    if webhook_info.url != config.WEBHOOK_URL:
        await sticker_bot.set_webhook(url=config.WEBHOOK_URL)


@app.post(config.WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    # Dispatcher.set_current(dispatcher)
    await dispatcher._process_update(sticker_bot, telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await sticker_bot.session.close()


@app.post("/sticker_pack")
async def sticker_pack_request(data: dict):
    token = data["token"]
    requests_data[token] = "some_data"
    return f"https://t.me/forthe_great_bot?start={token}"


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/exception_test")
async def error():
    raise Exception("Very bad things happened")
