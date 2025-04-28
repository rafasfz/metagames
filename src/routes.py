from fastapi import APIRouter
from src.domains.users.routes import users_router
from src.domains.authentication.routes import authentication_router

api = APIRouter(
    prefix="/api/v1/metagames",
)

api.include_router(router=users_router, tags=["users"])
api.include_router(router=authentication_router, tags=["authentication"])
