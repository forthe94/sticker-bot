import os
from pathlib import Path

import dotenv

PROJECT_ROOT: Path = Path(__file__).parent.parent

dotenv.load_dotenv(PROJECT_ROOT / ".env", verbose=True)

STICKER_BOT_TOKEN: str = os.getenv("STICKER_BOT_TOKEN", "")
ADMIN_TGS: list[int] = list(map(int, os.getenv("ADMIN_TGS", "259966720").split(",")))
