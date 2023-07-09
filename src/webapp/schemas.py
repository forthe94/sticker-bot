import dataclasses
import datetime
import uuid
from enum import Enum

from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.types import conlist


class StickerParams(BaseModel):
    background_img: str = Field(example="background.png")
    images: list[str] = Field(example=["car.png", "bus.png"])


class StickerPackRequest(BaseModel):
    token: uuid.UUID = Field(description="Idempotency token")
    name: str = Field(
        description="Stickerpack name",
        example="My beautiful stickerpack",
    )
    stickers: conlist(StickerParams, max_items=120)  # type: ignore


class ErrorCode(Enum):
    IMAGE_NOT_FOUND = "IMAGE_NOT_FOUND"
    STICKERS_AMOUNT_EXCEEDED = "STICKERS_AMOUNT_EXCEEDED"


class StickerPackRequestError(BaseModel):
    error_code: ErrorCode
    description: str


class ImageNotFoundError(StickerPackRequestError):
    error_code = ErrorCode.IMAGE_NOT_FOUND


class StickerAmountExceededError(StickerPackRequestError):
    error_code = ErrorCode.STICKERS_AMOUNT_EXCEEDED


class StickerPackResponse(BaseModel):
    success: bool
    first_req: bool = True
    bot_deeplink: str | None = Field(
        example="https://t.me/forthe_great_bot?start=<token_you_send>",
    )
    errors: list[ImageNotFoundError | StickerAmountExceededError] = Field(
        default_factory=list,
        description="Erros description",
    )


@dataclasses.dataclass
class SavedRequestData:
    data: StickerPackRequest
    user_id: str | None = None
    created_at: datetime.datetime = datetime.datetime.utcnow()
