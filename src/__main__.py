import uvicorn

from src.app import app


def main():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        access_log=True,
    )


if __name__ == "__main__":
    main()
