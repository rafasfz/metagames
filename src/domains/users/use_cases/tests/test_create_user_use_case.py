from typing import Generator
import pytest
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine
from pytest_alembic.runner import MigrationContext

from src.domains.users.entities import UserInputs
from src.domains.users.repositories.user_repository_orm import UserRepositoryORM
from src.domains.users.use_cases.create_user_use_case import (
    CreateUserUseCase,
    InputsCreateUserUseCase,
)
from src.infrastructure.db import Base
from src.resources.providers.exceptions_provider.exceptions_provider_http import (
    ExceptionsProviderHTTP,
)
from src.resources.providers.password_hasher.password_hasher_bcrypt import (
    PasswordHasherBCrypt,
)
from src.resources.providers.repositories_provider.repositories_provider_http import (
    RepositoriesProviderORM,
)


def test_create_user_use_case(
    engine: Engine, repositories_provider_orm: RepositoriesProviderORM
):
    user_inputs = UserInputs(
        email="john@doe.com",
        username="jonhndoe",
        password="password123",
        first_name="John",
        last_name="Doe",
    )

    inputs = InputsCreateUserUseCase(
        user=user_inputs,
    )

    outputs = CreateUserUseCase(
        user_repository=UserRepositoryORM(session=Session(engine)),
        password_hasher=PasswordHasherBCrypt(),
        exceptions_provider=ExceptionsProviderHTTP(),
    ).execute(inputs=inputs)

    created_user = repositories_provider_orm.user_respository.get_user_by_id(
        id=outputs.user.id,
    )

    assert outputs.user is not None
    assert created_user is not None

    assert created_user.id == outputs.user.id
    assert created_user.email == user_inputs.email
    assert created_user.username == user_inputs.username
    assert created_user.first_name == user_inputs.first_name
    assert created_user.last_name == user_inputs.last_name
