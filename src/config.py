import os
from pathlib import Path

import dotenv

PROJECT_ROOT: Path = Path(__file__).parent.parent
STATIC_DIR = PROJECT_ROOT / "static"
dotenv.load_dotenv(PROJECT_ROOT / ".env", verbose=True)

STICKER_BOT_TOKEN: str = os.getenv("STICKER_BOT_TOKEN", "")
STICKER_BOT_NAME: str = os.getenv("STICKER_BOT_NAME", "")
ADMIN_TGS: list[int] = list(map(int, os.getenv("ADMIN_TGS", "259966720").split(",")))
WEBHOOK_HOST: str = os.getenv(
    "WEBHOOK_HOST",
    "https://3146-5-152-51-131.ngrok-free.app",
)
WEBHOOK_PATH = f"/bot/{STICKER_BOT_TOKEN}"
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_PATH

BOT_TOKENS: list[str] = list(os.getenv("BOT_TOKENS", "").split(","))


STICKER_JSON_PATH = "/static/stickers.js"
