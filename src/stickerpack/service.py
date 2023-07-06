import io

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile
from PIL import Image

from src import config
from src.webapp import schemas


def create_sticker(sticker: schemas.StickerParams):
    background = Image.open(config.STATIC_DIR / sticker.background_img, "r")
    background = background.convert("RGBA")
    for image_file in sticker.images:
        image = Image.open(config.STATIC_DIR / image_file, "r")
        image = image.convert("RGBA")
        background = Image.alpha_composite(background, image)

    with io.BytesIO() as output:
        background.save(output, format="PNG")
        contents = output.getvalue()
    return contents


async def load_stickerpack_to_telegram(
    data: schemas.StickerPackRequest,
    user_id: int,
    bot: Bot,
):
    token_no_underlines = str(data.token).replace("-", "")
    set_name = f"set_{token_no_underlines}_by_{config.STICKER_BOT_NAME}"
    try:
        sticker_set = await bot.get_sticker_set(
            set_name,
        )
        return sticker_set
    except TelegramBadRequest:
        pass

    first_sticker = create_sticker(data.stickers[0])
    await bot.create_new_sticker_set(
        user_id,
        set_name,
        data.name,
        "\U0001F381",
        png_sticker=BufferedInputFile(
            first_sticker,
            filename=f"{token_no_underlines}_0.png",
        ),
    )
    idx = 1
    for sticker in data.stickers[1:]:
        await bot.add_sticker_to_set(
            user_id,
            set_name,
            "\U0001F381",
            png_sticker=BufferedInputFile(
                create_sticker(sticker),
                filename=f"{token_no_underlines}_{idx}.png",
            ),
        )
        idx += 1
    stickerset = await bot.get_sticker_set(
        set_name,
    )
    return stickerset
