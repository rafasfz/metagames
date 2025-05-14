from fastapi import APIRouter
from src.domains.users.routes import users_router
from src.domains.authentication.routes import sessions_router
from src.domains.games.routes import games_router

api = APIRouter(
    prefix="/api/v1/metagames",
)

api.include_router(router=users_router, tags=["users"])
api.include_router(router=sessions_router, tags=["sessions"])
api.include_router(router=games_router, tags=["games"])
