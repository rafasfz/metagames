import pytest

from src.domains.users.entities import UserEntity, UserInputs, UserRole
from src.domains.users.use_cases.create_user_use_case import (
    CreateUserUseCase,
    InputsCreateUserUseCase,
)


@pytest.fixture
def user_inputs() -> UserInputs:
    return UserInputs(
        email="john@doe.com",
        username="jonhndoe",
        password="password123",
        first_name="John",
        last_name="Doe",
    )


@pytest.fixture
def user_common() -> UserEntity:
    return UserEntity(
        email="user@common.com",
        username="user_common",
        first_name="User",
        last_name="Common",
        role=UserRole.USER,
    )


@pytest.fixture
def user_admin() -> UserEntity:
    return UserEntity(
        email="user@admin.com",
        username="user_admin",
        first_name="User",
        last_name="Admin",
        role=UserRole.ADMIN,
    )


@pytest.fixture
def registred_user(
    user_inputs: UserInputs,
    create_user_use_case: CreateUserUseCase,
) -> UserEntity:
    inputs = InputsCreateUserUseCase(
        user=user_inputs,
    )

    outputs = create_user_use_case.execute(
        inputs=inputs,
    )

    return outputs.user
