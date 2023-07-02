# from src.bot.bot import sticker_bot
#
#
# async def load_stickerpack_to_telegram():
#     bot_name = await sticker_bot.get_me()
#     res = await sticker_bot.create_new_sticker_set(
#         259966720,
#         f'custom_by_{bot_name.username}',
#         'Test',
#         '\U0001F381',
#         png_sticker=aiogram.types.FSInputFile('static/1.png')
#     )
#     stickerset = await sticker_bot.get_sticker_set("custom_by_talent_forthe_bot")
#     await sticker_bot.send_sticker(259966720, stickerset.stickers[0].file_id)
#
#
# import asyncio
#
#
# async def main():
#     await load_stickerpack_to_telegram()
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
