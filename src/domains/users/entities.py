from pydantic import BaseModel, EmailStr, Field
from enum import Enum

from src.resources.abstracts.entities import AbstractEntity


class UserRole(str, Enum):
    USER = "user"
    COMPANY = "company"
    ADMIN = "admin"


class UserData(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    email: EmailStr = Field()
    first_name: str = Field(min_length=3, max_length=32)
    last_name: str = Field(min_length=3, max_length=128)
    role: UserRole = Field(default=UserRole.USER)


class UserWithPasswordHash(UserData):
    password_hash: str = Field()


class UserEntity(UserData, AbstractEntity):
    pass
