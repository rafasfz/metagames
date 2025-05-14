from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, status

from src.domains.authentication.routes import get_user_if_authenticated
from src.domains.users.entities import UserEntity
from src.domains.users.use_cases.create_user_use_case import (
    CreateUserUseCase,
    InputsCreateUserUseCase,
    OutputsCreateUserUseCase,
)
from src.domains.users.use_cases.get_user_by_id_use_case import (
    GetUserByIdUseCase,
    InputsGetUserByIdUseCase,
    OutputsGetUserByIdUseCase,
)
from src.resources.providers.exceptions_provider.exceptions_provider_http import (
    ExceptionsProviderHTTP,
)
from src.resources.providers.password_hasher.password_hasher_bcrypt import (
    PasswordHasherBCrypt,
)
from src.resources.providers.repositories_provider.repositories_provider_orm import (
    RepositoriesProviderORM,
)

users_router = APIRouter(
    prefix="/users",
)


@users_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    inputs: InputsCreateUserUseCase,
    user: Annotated[UserEntity | None, Depends(get_user_if_authenticated)],
) -> OutputsCreateUserUseCase:

    outputs = CreateUserUseCase(
        authenticated_user=user,
        repositories_provider=RepositoriesProviderORM(),
        password_hasher=PasswordHasherBCrypt(),
        exceptions_provider=ExceptionsProviderHTTP(),
    ).execute(inputs=inputs)

    return outputs


@users_router.get("/{id}")
def get_user_by_id(id: UUID) -> OutputsGetUserByIdUseCase:

    outputs = GetUserByIdUseCase(
        repositories_provider=RepositoriesProviderORM(),
        exceptions_provider=ExceptionsProviderHTTP(),
    ).execute(inputs=InputsGetUserByIdUseCase(id=id))

    return outputs
