from src.domains.authentication.exceptions.authentications_exceptions_http import (
    AuthenticationExceptionsHTTP,
)
from src.domains.users.exceptions.user_exceptions_http import UserExceptionsHTTP
from src.resources.providers.exceptions_provider.exceptions_provider import (
    ExceptionsProvider,
)


class ExceptionsProviderHTTP(ExceptionsProvider):
    user_exceptions: UserExceptionsHTTP = UserExceptionsHTTP()
    authentication_exceptions: AuthenticationExceptionsHTTP = (
        AuthenticationExceptionsHTTP()
    )
