from pydantic import BaseModel, Field
from src.resources.abstracts.entities import AbstractEntity


class PlatformData(BaseModel):
    name: str = Field(min_length=3, max_length=256)


class PlatformEntity(PlatformData, AbstractEntity):
    games: list["GameEntity"] = Field(default_factory=list)


class GameData(BaseModel):
    name: str = Field(min_length=3, max_length=256)
    description: str = Field(min_length=3, max_length=2048)


class GameEntity(GameData, AbstractEntity):
    platforms: list[PlatformEntity] = Field(default_factory=list)
