import pytest
from typing import Generator
from sqlalchemy import Engine
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
def repositories_provider_orm(engine: Engine) -> RepositoriesProviderORM:
    return RepositoriesProviderORM(
        user_repository=UserRepositoryORM(session=Session(engine)),
    )
