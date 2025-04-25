from abc import ABC, abstractmethod
from uuid import UUID


class UserExceptions(ABC):

    @abstractmethod
    def user_already_exists(self, field: str) -> Exception:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def user_not_found(self, id: UUID) -> Exception:
        raise NotImplementedError("Method not implemented")
