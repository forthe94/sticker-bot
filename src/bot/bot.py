import traceback
from typing import Any, Awaitable, Callable

import aiogram
from aiogram import BaseMiddleware, Bot, Dispatcher, types
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message
from sqlitedict import SqliteDict

from src import config
from src.stickerpack import service
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
    try:
        if command.args is None:
            await message.answer(
                "Этот праздник очень важен для сотрудников ритейла, "
                "поэтому мы предлагаем вам создать собственный набор стикеров и "
                "поздравить коллег и друзей с праздником! "
                "Это легко: просто перейдите на сайт и создайте свой стикерпак!",
                reply_markup=types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [
                            types.InlineKeyboardButton(
                                text="Перейти",
                                url="https://vps-retailday.socialcraft.ru/",
                            ),
                        ],
                    ],
                ),
            )
            return

        token_no_underlines = str(requests_data[command.args].data.token).replace(
            "-",
            "",
        )
        set_name = f"set_{token_no_underlines}_by_{config.STICKER_BOT_NAME}"
        stickerset = None
        try:
            stickerset = await sticker_bot.get_sticker_set(
                set_name,
            )
        except aiogram.exceptions.TelegramBadRequest:
            pass

        if stickerset:
            keyboard = types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        types.InlineKeyboardButton(
                            text="Открыть набор стикеров",
                            url=f"t.me/addstickers/{stickerset.name}",
                        ),
                    ],
                ],
            )
            await message.answer_sticker(
                stickerset.stickers[0].file_id,
                reply_markup=keyboard,
            )
            return

        await message.answer(
            "Ваш набор стикеров уже создан, но нужно подождать ещё совсем немного, "
            "и вашим близким будет приятно ваше внимание 🔥",
        )

        requests_data[command.args].user_id = message.from_user.id
        requests_data.commit()

        stickerset = await service.create_stickerpack(
            requests_data[command.args].data,
            message.from_user.id,
            sticker_bot,
        )
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Открыть набор стикеров",
                        url=f"t.me/addstickers/{stickerset.name}",
                    ),
                ],
            ],
        )
        await message.answer_sticker(
            stickerset.stickers[0].file_id,
            reply_markup=keyboard,
        )

        await service.add_stickers_to_stickerpack(
            requests_data[command.args].data,
            message.from_user.id,
            sticker_bot,
            stickerset,
        )

    except Exception:
        await message.answer("Ой, что-то пошло не так \U0001F61E")
        raise


@dispatcher.message()
async def any(message: types.Message):
    await message.answer(
        "Этот праздник очень важен для сотрудников ритейла, поэтому мы предлагаем вам "
        "создать собственный набор стикеров и поздравить коллег и друзей с праздником! "
        "Это легко: просто перейдите на сайт и создайте свой стикерпак!",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Перейти",
                        url="https://vps-retailday.socialcraft.ru/",
                    ),
                ],
            ],
        ),
    )
