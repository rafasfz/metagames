from abc import ABC

from src.domains.authentication.exceptions.authentication_exceptions import (
    AuthenticationExceptions,
)
from src.domains.users.exceptions.user_exceptions import UserExceptions


class ExceptionsProvider(ABC):
    user_exceptions: UserExceptions
    authentication_exceptions: AuthenticationExceptions
