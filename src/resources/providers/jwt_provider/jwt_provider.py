from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional

from pydantic import BaseModel

from src.domains.users.entities import UserEntity


class Payload(BaseModel):
    user: UserEntity
    exp: Optional[int] = None


class JWTProvider(ABC):
    @abstractmethod
    def generate_token(
        self, user: UserEntity, expires_in: Optional[timedelta] = None
    ) -> str:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def verify_token(self, token: str) -> Payload:
        raise NotImplementedError("Method not implemented")
