import os
import traceback
from typing import Awaitable, Callable

from fastapi import Request, Response

from src import config
from src.bot.bot import sticker_bot
from src.webapp.admin import notify_admins


def generate_sticker_json_file() -> None:
    js_stickers = "window.stickers = {\n"
    js_stickers += "    image: [\n"
    for bg_im in os.listdir(config.STATIC_DIR / "background"):
        js_stickers += " " * 8 + config.WEBHOOK_HOST + "static/background/" + bg_im + "\n"
    js_stickers += "],\n\n"

    js_stickers += "    emoji: [\n"
    for emoji in os.listdir(config.STATIC_DIR / "emoji"):
        js_stickers += " " * 8 + config.WEBHOOK_HOST + "static/emoji/" + emoji + "\n"

    js_stickers += "],\n\n"

    js_stickers += "    label: [\n"
    for label in os.listdir(config.STATIC_DIR / "label"):
        js_stickers += " " * 8 + config.WEBHOOK_HOST + "static/label/" + label + "\n"

    js_stickers += "]\n}"

    with open(config.PROJECT_ROOT / config.STICKER_JSON_PATH[1:], "w") as f:
        f.write(js_stickers)


async def log_errors_to_tg(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    try:
        return await call_next(request)
    except Exception as e:
        await notify_admins(
            "".join(traceback.format_exception(e)),
            sticker_bot,
        )
        raise


async def create_stickers_json_file(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    if request.scope["path"] == config.STICKER_JSON_PATH:
        generate_sticker_json_file()

    return await call_next(request)
