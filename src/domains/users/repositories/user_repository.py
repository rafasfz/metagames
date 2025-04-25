from abc import ABC, abstractmethod
from uuid import UUID

from src.domains.users.entities import UserEntity, UserToSave


class UserRepository(ABC):

    @abstractmethod
    def create_user(self, user: UserToSave) -> UserEntity:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_user_by_email(self, email: str) -> UserEntity | None:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_user_by_username(self, username: str) -> UserEntity | None:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def get_user_by_id(self, id: UUID) -> UserEntity | None:
        raise NotImplementedError("Method not implemented")
