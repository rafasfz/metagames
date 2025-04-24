from abc import ABC, abstractmethod

from src.domains.users.entities import UserEntity, UserWithPasswordHash


class UserRepository(ABC):

    @abstractmethod
    def create_user(self, user: UserWithPasswordHash) -> UserEntity:
        raise NotImplementedError("Method not implemented")
