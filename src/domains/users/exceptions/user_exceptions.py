from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import HTTPException


class UserExceptions(ABC):

    @abstractmethod
    def user_already_exists(self, field: str) -> HTTPException:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def user_not_found(self, id: UUID) -> HTTPException:
        raise NotImplementedError("Method not implemented")
