from datetime import datetime
from uuid import UUID, uuid4
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


class UserInputs(UserData):
    password: str = Field(min_length=8, max_length=128)


class UserToSave(UserData):
    id: UUID = Field(default_factory=uuid4)
    password_hash: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class UserEntity(UserData, AbstractEntity):
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    def is_company(self) -> bool:
        return self.role == UserRole.COMPANY

    pass
