from fastapi import FastAPI

from src.webapp.middleware import log_errors_to_tg

app = FastAPI()

app.add_middleware(log_errors_to_tg)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/exception_test")
async def error():
    raise Exception("Very bad things happened")
    return {"message": "Hello World"}
