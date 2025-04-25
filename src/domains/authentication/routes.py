from fastapi import APIRouter, status

from src.domains.authentication.exceptions.authentications_exceptions_http import (
    AuthenticationExceptionsHTTP,
)
from src.domains.authentication.use_cases.login_use_case import (
    InputsLoginUseCase,
    LoginUseCase,
    OutputsLoginUseCase,
)
from src.domains.users.repositories.user_repository_orm import UserRepositoryORM
from src.resources.providers.jwt_provider.py_jwt_provider import PyJWTProvider
from src.resources.providers.password_hasher.password_hasher_bcrypt import (
    PasswordHasherBCrypt,
)

authentication_router = APIRouter(
    prefix="/authentication",
)


@authentication_router.post("/", status_code=status.HTTP_200_OK)
def login_user(inputs: InputsLoginUseCase) -> OutputsLoginUseCase:

    outputs = LoginUseCase(
        user_repository=UserRepositoryORM(),
        password_hasher=PasswordHasherBCrypt(),
        jwt_provider=PyJWTProvider(),
        authentication_exceptions=AuthenticationExceptionsHTTP(),
    ).execute(inputs=inputs)

    return outputs
