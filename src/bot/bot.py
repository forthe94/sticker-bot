from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandObject, CommandStart
from sqlitedict import SqliteDict

from src import config
from src.stickerpack.service import load_stickerpack_to_telegram
from src.webapp.admin import notify_admins

sticker_bot = Bot(token=config.STICKER_BOT_TOKEN)
requests_data = SqliteDict("req_data.sqlite")
dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def start(message: types.Message, command: CommandObject) -> None:
    ans_mes = await message.answer("Стикеры создаются!")

    if command.args is None:
        await notify_admins("Empty command args", sticker_bot)
        return

    data = requests_data[command.args]
    stickerset = await load_stickerpack_to_telegram(
        data,
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
