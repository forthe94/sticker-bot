from aiogram import Bot

from src import config


async def notify_admins(msg: str, bot: Bot) -> None:
    for admin in config.ADMIN_TGS:
        await bot.send_message(
            admin,
            msg,
        )
