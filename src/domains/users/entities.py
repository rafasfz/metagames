from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from enum import Enum

from src.resources.abstracts.entity import AbstractEntity


class UserRole(str, Enum):
    USER = "user"
    COMPANY = "company"
    ADMIN = "admin"


class UserEntity(AbstractEntity):
    username: str = Field(min_length=3, max_length=32)
    email: EmailStr = Field()
    first_name: str = Field(min_length=3, max_length=32)
    last_name: str = Field(min_length=3, max_length=128)
    role: UserRole = Field(default=UserRole.USER)
