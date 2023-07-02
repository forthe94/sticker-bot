from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/exception_test")
async def error():
    raise Exception("Very bad things happened")
    return {"message": "Hello World"}
