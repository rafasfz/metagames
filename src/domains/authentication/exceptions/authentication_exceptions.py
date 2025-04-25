from abc import ABC, abstractmethod


class AuthenticationExceptions(ABC):

    @abstractmethod
    def invalid_credentials(self):
        raise NotImplementedError("Method not implemented")
