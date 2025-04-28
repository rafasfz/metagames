from typing import Generator
import pytest
from sqlalchemy import Engine

from src.domains.users.entities import UserEntity, UserInputs, UserRole
from src.domains.users.repositories.user_repository_orm import UserRepositoryORM
from src.infrastructure.db import Base
from src.resources.providers.repositories_provider.repositories_provider_orm import (
    RepositoriesProviderORM,
)
from sqlalchemy.orm import Session


@pytest.fixture
def engine(alembic_engine: Engine) -> Generator[Engine, None, None]:
    Base.metadata.create_all(alembic_engine)

    yield alembic_engine

    alembic_engine.dispose()


@pytest.fixture
def repositories_provider_orm(engine) -> RepositoriesProviderORM:
    return RepositoriesProviderORM(
        user_repository=UserRepositoryORM(session=Session(engine)),
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
