from fastapi import FastAPI
from src.routes import api


app = FastAPI()

app.include_router(router=api)


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
