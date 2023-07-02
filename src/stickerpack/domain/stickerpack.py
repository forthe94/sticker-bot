from pydantic import BaseModel


class Image(BaseModel):
    name: str
    pos_x: int
    pos_y: int


class Sticker(BaseModel):
    background: Image
    overlay_images: list[Image]


class StickerPack(BaseModel):
    name: str
    title: str
    stickers: list[Sticker]
