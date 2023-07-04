from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandObject, CommandStart

from src import config

sticker_bot = Bot(token=config.STICKER_BOT_TOKEN)
requests_data = {}
dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def echo_handler(message: types.Message, command: CommandObject) -> None:
    await message.answer(requests_data[command.args])
