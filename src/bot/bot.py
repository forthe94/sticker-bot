import traceback
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot, Dispatcher, types
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message
from sqlitedict import SqliteDict

from src import config
from src.stickerpack.service import load_stickerpack_to_telegram
from src.webapp.admin import notify_admins

sticker_bot = Bot(token=config.STICKER_BOT_TOKEN)
requests_data = SqliteDict("data/req_data.sqlite")
dispatcher = Dispatcher()


class ErrorLogMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            await notify_admins(
                "".join(traceback.format_exception(e)),
                sticker_bot,
            )
            raise


dispatcher.message.middleware(ErrorLogMiddleware())


@dispatcher.message(CommandStart())
async def start(message: types.Message, command: CommandObject) -> None:
    ans_mes = await message.answer("Стикеры создаются!")
    try:
        if command.args is None:
            await notify_admins("Empty command args", sticker_bot)
            return

        requests_data[command.args].user_id = message.from_user.id
        requests_data.commit()

        stickerset = await load_stickerpack_to_telegram(
            requests_data[command.args].data,
            message.from_user.id,
            sticker_bot,
        )

        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Ваш стикерпак",
                        url=f"t.me/addstickers/{stickerset.name}",
                    ),
                ],
            ],
        )
        await ans_mes.edit_text("Готово!", reply_markup=keyboard)
    except Exception:
        await message.answer("Ой, что-то пошло не так \U0001F61E")
        raise
