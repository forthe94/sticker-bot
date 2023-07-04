import argparse
import asyncio

import uvicorn

from src.bot.bot import dispatcher, sticker_bot
from src.webapp.app import app


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "command",
        choices=["api", "bot", "api+bot"],
        help="Command to execute",
    )
    args = arg_parser.parse_args()

    match args.command:
        case "api":
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=8000,
                access_log=True,
            )
        case "bot":
            asyncio.run(dispatcher.run_polling(sticker_bot))
        case "api+bot":
            asyncio.run(dispatcher.start_polling(sticker_bot))
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=8000,
                access_log=True,
            )


if __name__ == "__main__":
    main()
