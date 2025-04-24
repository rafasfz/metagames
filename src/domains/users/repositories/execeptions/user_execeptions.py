from abc import ABC, abstractmethod


class UserExceptions(ABC):

    @abstractmethod
    def user_already_exists(self, field: str) -> Exception:
        raise NotImplementedError("Method not implemented")
