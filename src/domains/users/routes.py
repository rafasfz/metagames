from uuid import UUID
from fastapi import APIRouter, status

from src.domains.users.repositories.execeptions.user_execeptions_http import (
    UserExceptionsHTTP,
)
from src.domains.users.repositories.user_repository_orm import UserRepositoryORM
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
from src.resources.password_hasher.password_hasher_bcrypt import (
    PasswordHasherProviderBCrypt,
)

users_router = APIRouter(
    prefix="/users",
)


@users_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(inputs: InputsCreateUserUseCase) -> OutputsCreateUserUseCase:

    outputs = CreateUserUseCase(
        user_repository=UserRepositoryORM(),
        user_exceptions=UserExceptionsHTTP(),
        password_hasher=PasswordHasherProviderBCrypt(),
    ).execute(inputs=inputs)

    return outputs


@users_router.get("/{id}")
def get_user_by_id(id: UUID) -> OutputsGetUserByIdUseCase:

    outputs = GetUserByIdUseCase(
        user_repository=UserRepositoryORM(), user_exceptions=UserExceptionsHTTP()
    ).execute(inputs=InputsGetUserByIdUseCase(id=id))

    return outputs
