# import traceback
# import uuid
#
# import aiogram
# from aiogram.exceptions import (TelegramBadRequest, TelegramNetworkError,
#                                 TelegramRetryAfter)
#
# from src.bot.bot import sticker_bot
#
#
# async def load_stickerpack_to_telegram():
#     bot = sticker_bot
#     user_id = 5453614047
#     for i in range(500, 1000):
#         print(f"Try with bot {bot.token}, id {user_id}")
#         bot_name = await bot.get_me()
#         uuid_num = uuid.uuid4().hex
#         res = await bot.create_new_sticker_set(
#             user_id,
#             f"custom_{uuid_num}_by_{bot_name.username}",
#             f"{uuid_num} by @{bot_name.username}",
#             "\U0001F381",
#             png_sticker=aiogram.types.FSInputFile(f"static/{i % 3 + 1}.png"),
#             # png_sticker=sticker_file.file_id,
#             request_timeout=10,
#         )
#         stickerset = await bot.get_sticker_set(
#             f"custom_{uuid_num}_by_{bot_name.username}",
#         )
#         await bot.send_sticker(user_id, stickerset.stickers[0].file_id)
#         # await bot.send_message(259966720, i)
#         print(f"Send {i}")
