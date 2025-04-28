from typing import Generator
import pytest
from sqlalchemy import Engine

from src.domains.users.repositories.user_repository_orm import UserRepositoryORM
from src.infrastructure.db import Base
from src.resources.providers.repositories_provider.repositories_provider_http import (
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
        user_respository=UserRepositoryORM(session=Session(engine)),
    )
