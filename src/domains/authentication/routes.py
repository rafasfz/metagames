from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

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
from src.resources.providers.exceptions_provider.exceptions_provider_http import (
    ExceptionsProviderHTTP,
)
from src.resources.providers.jwt_provider.py_jwt_provider import PyJWTProvider
from src.resources.providers.password_hasher.password_hasher_bcrypt import (
    PasswordHasherBCrypt,
)
from src.resources.providers.repositories_provider.repositories_provider_orm import (
    RepositoriesProviderORM,
)

sessions_router = APIRouter(
    prefix="/sessions",
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


@sessions_router.post("/", status_code=status.HTTP_200_OK)
def login_user(inputs: InputsLoginUseCase) -> OutputsLoginUseCase:

    outputs = LoginUseCase(
        password_hasher=PasswordHasherBCrypt(),
        jwt_provider=PyJWTProvider(),
        repositories_provider=RepositoriesProviderORM(),
        exceptions_provider=ExceptionsProviderHTTP(),
    ).execute(inputs=inputs)

    return outputs
