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


@pytest.fixture
def engine(alembic_engine: Engine) -> Generator[Engine, None, None]:
    Base.metadata.create_all(alembic_engine)

    yield alembic_engine

    alembic_engine.dispose()


def test_create_user_use_case(engine: Engine):
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

    assert outputs.user.id is not None
