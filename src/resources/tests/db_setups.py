import pytest
from typing import Generator
from sqlalchemy import Engine
from src.domains.games.repositories.platform_repository_alchemy import (
    PlatformRepositoryAlchemy,
)
from src.domains.users.repositories.user_repository_orm import UserRepositoryORM
from src.infrastructure.db import Base
from src.resources.providers.repositories_provider.repositories_provider_orm import (
    RepositoriesProviderORM,
)
from sqlalchemy.orm import Session


@pytest.fixture
def in_memory_db() -> Generator[Engine, None, None]:
    from sqlalchemy import create_engine

    engine = create_engine("sqlite:///:memory:", echo=True)
    yield engine
    engine.dispose()


@pytest.fixture
def engine(in_memory_db: Engine) -> Generator[Engine, None, None]:
    Base.metadata.create_all(in_memory_db)

    yield in_memory_db

    in_memory_db.dispose()


@pytest.fixture
def repositories_provider_orm(engine: Engine) -> RepositoriesProviderORM:
    return RepositoriesProviderORM(
        user_repository=UserRepositoryORM(session=Session(engine)),
        platform_repository=PlatformRepositoryAlchemy(session=Session(engine)),
    )
