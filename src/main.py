from fastapi import APIRouter, FastAPI
from src.domains.users.routes import users_router
from src.domains.authentication.routes import authentication_router

app = FastAPI()

api = APIRouter(
    prefix="/api/v1/metagames",
    tags=["api"],
)

api.include_router(router=users_router)
api.include_router(router=authentication_router)

app.include_router(router=api)


@app.get("/ping")
def ping():
    return {"ping": "pong!"}
