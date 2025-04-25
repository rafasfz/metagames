from fastapi import HTTPException
from src.domains.authentication.exceptions.authentication_exceptions import (
    AuthenticationExceptions,
)


class AuthenticationExceptionsHTTP(AuthenticationExceptions):

    def invalid_credentials(self):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )
