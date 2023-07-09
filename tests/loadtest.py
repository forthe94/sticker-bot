import asyncio

from src.stickerpack.service import create_sticker
from src.webapp import schemas


async def main():
    for idx in range(500):
        sticker = schemas.StickerParams(
            background_img="1.png",
            images=["2.png", "3.png"],
        )
        sticker = create_sticker(sticker)
        print(idx, sticker[0])


if __name__ == "__main__":
    asyncio.run(main())
