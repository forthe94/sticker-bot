import os

from aiogram import types
from fastapi import FastAPI
from loguru import logger

from src import config
from src.bot.bot import dispatcher, requests_data, sticker_bot
from src.webapp import schemas
from src.webapp.middleware import log_errors_to_tg

app = FastAPI(title="Stickerpack API")

app.middleware("HTTP")(log_errors_to_tg)


@app.on_event("startup")
async def on_startup():
    webhook_info = await sticker_bot.get_webhook_info()
    if webhook_info.url != config.WEBHOOK_URL:
        await sticker_bot.set_webhook(url=config.WEBHOOK_URL)


@app.post(config.WEBHOOK_PATH, include_in_schema=False)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    # Dispatcher.set_current(dispatcher)
    await dispatcher._process_update(sticker_bot, telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await sticker_bot.session.close()


@app.post("/sticker_pack")
async def sticker_pack_request(
    data: schemas.StickerPackRequest,
) -> schemas.StickerPackResponse:
    token = data.token
    deeplink = f"https://t.me/{config.STICKER_BOT_NAME}?start={token}"
    if str(token) in requests_data:
        return schemas.StickerPackResponse(
            success=True,
            first_req=False,
            bot_deeplink=deeplink,
        )
    requests_data[str(token)] = data
    requests_data.commit()

    errors = []
    static_files_on_server = os.listdir(config.STATIC_DIR)
    logger.info("New stickerpack request {}", token)
    for sticker in data.stickers:
        for image in sticker.images + [sticker.background_img]:
            if image not in static_files_on_server:
                errors.append(
                    schemas.ImageNotFoundError(
                        description=image,
                    ),
                )
    if errors:
        success = False
        deeplink = None
    else:
        success = True
        deeplink = f"https://t.me/{config.STICKER_BOT_NAME}?start={token}"
    logger.info(
        "Response success:{}, deeplink:{}, errors:{}",
        success,
        deeplink,
        errors,
    )
    resp = schemas.StickerPackResponse(
        success=success,
        bot_deeplink=deeplink,
        errors=errors,
    )
    return resp


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/exception_test")
async def error():
    raise Exception("Very bad things happened")
