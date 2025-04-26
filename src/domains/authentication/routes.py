from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domains.authentication.exceptions.authentications_exceptions_http import (
    AuthenticationExceptionsHTTP,
)
from src.domains.authentication.use_cases.get_user_if_authenticated_use_case import (
    GetUserIfAuthenticatedUseCase,
    InputsGetUserIfAuthenticatedUseCase,
)
from src.domains.authentication.use_cases.login_use_case import (
    InputsLoginUseCase,
    LoginUseCase,
    OutputsLoginUseCase,
)
from src.domains.users.entities import UserEntity
from src.domains.users.repositories.user_repository_orm import UserRepositoryORM
from src.resources.providers.jwt_provider.py_jwt_provider import PyJWTProvider
from src.resources.providers.password_hasher.password_hasher_bcrypt import (
    PasswordHasherBCrypt,
)

authentication_router = APIRouter(
    prefix="/authentication",
)

auth_scheme = HTTPBearer(auto_error=False)


def get_user_if_authenticated(
    auth_credentials: Annotated[HTTPAuthorizationCredentials, Depends(auth_scheme)],
) -> UserEntity | None:
    token = auth_credentials.credentials if auth_credentials else ""

    user = (
        GetUserIfAuthenticatedUseCase(
            jwt_provider=PyJWTProvider(),
        )
        .execute(
            inputs=InputsGetUserIfAuthenticatedUseCase(
                token=token,
            )
        )
        .user
    )

    return user


@authentication_router.post("/", status_code=status.HTTP_200_OK)
def login_user(inputs: InputsLoginUseCase) -> OutputsLoginUseCase:

    outputs = LoginUseCase(
        user_repository=UserRepositoryORM(),
        password_hasher=PasswordHasherBCrypt(),
        jwt_provider=PyJWTProvider(),
        authentication_exceptions=AuthenticationExceptionsHTTP(),
    ).execute(inputs=inputs)

    return outputs
