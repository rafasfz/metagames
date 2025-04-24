from abc import ABC, abstractmethod

from src.domains.users.entities import UserEntity, UserToSave


class UserRepository(ABC):

    @abstractmethod
    def create_user(self, user: UserToSave) -> UserEntity:
        raise NotImplementedError("Method not implemented")
