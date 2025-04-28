from typing import Callable
from fastapi import HTTPException
import pytest
from src.domains.users.entities import UserEntity, UserInputs, UserRole
from src.domains.users.use_cases.create_user_use_case import (
    CreateUserUseCase,
    InputsCreateUserUseCase,
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
def create_user(
    repositories_provider_orm: RepositoriesProviderORM,
) -> Callable[[UserInputs], None]:
    def _create_user(user: UserInputs):
        inputs = InputsCreateUserUseCase(
            user=user,
        )

        CreateUserUseCase(
            repositories_provider=repositories_provider_orm,
            password_hasher=PasswordHasherBCrypt(),
            exceptions_provider=ExceptionsProviderHTTP(),
        ).execute(inputs=inputs)

    return _create_user


def test_create_user_use_case(
    user_inputs: UserInputs, repositories_provider_orm: RepositoriesProviderORM
):
    inputs = InputsCreateUserUseCase(
        user=user_inputs,
    )

    outputs = CreateUserUseCase(
        repositories_provider=repositories_provider_orm,
        password_hasher=PasswordHasherBCrypt(),
        exceptions_provider=ExceptionsProviderHTTP(),
    ).execute(inputs=inputs)

    created_user = repositories_provider_orm.user_repository.get_user_by_id(
        id=outputs.user.id,
    )

    assert outputs.user is not None
    assert created_user is not None

    assert created_user.id == outputs.user.id
    assert created_user.email == user_inputs.email
    assert created_user.username == user_inputs.username
    assert created_user.first_name == user_inputs.first_name
    assert created_user.last_name == user_inputs.last_name


def test_create_user_use_case_with_existing_email(
    user_inputs: UserInputs,
    repositories_provider_orm: RepositoriesProviderORM,
    create_user: Callable[[UserInputs], None],
):
    user_inputs.username = "new_username"
    inputs = InputsCreateUserUseCase(
        user=user_inputs,
    )

    create_user(user_inputs)

    with pytest.raises(HTTPException) as http_exception:
        CreateUserUseCase(
            repositories_provider=repositories_provider_orm,
            password_hasher=PasswordHasherBCrypt(),
            exceptions_provider=ExceptionsProviderHTTP(),
        ).execute(inputs=inputs)

    assert http_exception.value.status_code == 400


def test_create_user_use_case_with_existing_username(
    user_inputs: UserInputs,
    repositories_provider_orm: RepositoriesProviderORM,
    create_user: Callable[[UserInputs], None],
):
    user_inputs.email = "another@email.com"
    inputs = InputsCreateUserUseCase(
        user=user_inputs,
    )

    create_user(user_inputs)

    with pytest.raises(HTTPException) as http_exception:
        CreateUserUseCase(
            repositories_provider=repositories_provider_orm,
            password_hasher=PasswordHasherBCrypt(),
            exceptions_provider=ExceptionsProviderHTTP(),
        ).execute(inputs=inputs)

    assert http_exception.value.status_code == 400


def test_create_admin_user_with_not_admin_user(
    repositories_provider_orm: RepositoriesProviderORM,
    user_inputs: UserInputs,
    user_common: UserEntity,
):
    user_inputs.role = UserRole.ADMIN

    inputs = InputsCreateUserUseCase(
        user=user_inputs,
    )

    outputs = CreateUserUseCase(
        repositories_provider=repositories_provider_orm,
        password_hasher=PasswordHasherBCrypt(),
        exceptions_provider=ExceptionsProviderHTTP(),
        user=user_common,
    ).execute(inputs=inputs)

    assert outputs.user.role == UserRole.USER

    created_user = repositories_provider_orm.user_repository.get_user_by_id(
        id=outputs.user.id,
    )

    assert created_user is not None
    assert created_user.role == UserRole.USER


def test_create_admin_user_with_admin_user(
    repositories_provider_orm: RepositoriesProviderORM,
    user_inputs: UserInputs,
    user_admin: UserEntity,
):
    user_inputs.role = UserRole.ADMIN

    inputs = InputsCreateUserUseCase(
        user=user_inputs,
    )

    outputs = CreateUserUseCase(
        repositories_provider=repositories_provider_orm,
        password_hasher=PasswordHasherBCrypt(),
        exceptions_provider=ExceptionsProviderHTTP(),
        user=user_admin,
    ).execute(inputs=inputs)

    assert outputs.user.role == UserRole.ADMIN

    created_user = repositories_provider_orm.user_repository.get_user_by_id(
        id=outputs.user.id,
    )

    assert created_user is not None
    assert created_user.role == UserRole.ADMIN


def test_create_company_user_with_admin_user(
    repositories_provider_orm: RepositoriesProviderORM,
    user_inputs: UserInputs,
    user_admin: UserEntity,
):
    user_inputs.role = UserRole.COMPANY

    inputs = InputsCreateUserUseCase(
        user=user_inputs,
    )

    outputs = CreateUserUseCase(
        repositories_provider=repositories_provider_orm,
        password_hasher=PasswordHasherBCrypt(),
        exceptions_provider=ExceptionsProviderHTTP(),
        user=user_admin,
    ).execute(inputs=inputs)

    assert outputs.user.role == UserRole.COMPANY

    created_user = repositories_provider_orm.user_repository.get_user_by_id(
        id=outputs.user.id,
    )

    assert created_user is not None
    assert created_user.role == UserRole.COMPANY
