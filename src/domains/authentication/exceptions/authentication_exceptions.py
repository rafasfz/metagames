from abc import ABC, abstractmethod


class AuthenticationExceptions(ABC):

    @abstractmethod
    def invalid_credentials(self) -> Exception:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def invalid_token(self) -> Exception:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def unauthorized(self) -> Exception:
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    def forbidden(self) -> Exception:
        raise NotImplementedError("Method not implemented")
