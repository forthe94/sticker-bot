import traceback
from typing import Awaitable, Callable

from fastapi import Request, Response

from src.bot.bot import sticker_bot
from src.webapp.admin import notify_admins


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
