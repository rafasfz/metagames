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

users_router = APIRouter(
    prefix="/users",
)


@users_router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(inputs: InputsCreateUserUseCase) -> OutputsCreateUserUseCase:

    outputs = CreateUserUseCase(
        user_repository=UserRepositoryORM(), user_exceptions=UserExceptionsHTTP()
    ).execute(inputs=inputs)

    return outputs
