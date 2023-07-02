import traceback
from typing import Awaitable, Callable

from fastapi import Request, Response

from src import config
from src.bot.bot import sticker_bot
from src.webapp.app import app


@app.middleware("http")
async def add_process_time_header(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    try:
        return await call_next(request)
    except Exception as e:
        for admin in config.ADMIN_TGS:
            await sticker_bot.send_message(
                admin,
                "".join(traceback.format_exception(e)),
            )
        raise
