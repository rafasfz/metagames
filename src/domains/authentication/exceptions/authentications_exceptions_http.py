from fastapi import HTTPException
from src.domains.authentication.exceptions.authentication_exceptions import (
    AuthenticationExceptions,
)


class AuthenticationExceptionsHTTP(AuthenticationExceptions):

    def invalid_credentials(self) -> Exception:
        return HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    def invalid_token(self) -> Exception:
        return HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    def unauthorized(self) -> Exception:
        return HTTPException(
            status_code=401,
            detail="Unauthorized",
        )

    def forbidden(self) -> Exception:
        return HTTPException(
            status_code=403,
            detail="Forbidden",
        )
