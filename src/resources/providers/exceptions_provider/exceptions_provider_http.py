from src.resources.providers.exceptions_provider import exceptions_provider


class ExceptionsProvider(exceptions_provider):
    user_exceptions: UserExceptionsHTTP
    authentication_exceptions: AuthenticationExceptionsHTTP
