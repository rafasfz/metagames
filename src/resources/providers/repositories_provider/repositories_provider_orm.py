from dataclasses import dataclass
from sqlalchemy.orm import Session

from src.domains.games.repositories.platform_repository_alchemy import (
    PlatformRepositoryAlchemy,
)
from src.infrastructure.db import engine
from src.domains.users.repositories.user_repository_orm import UserRepositoryORM
from src.resources.providers.repositories_provider.repositories_provider import (
    RepositoriesProvider,
)


@dataclass
class RepositoriesProviderORM(RepositoriesProvider):
    user_repository: UserRepositoryORM = UserRepositoryORM(Session(engine))
    platform_repository: PlatformRepositoryAlchemy = PlatformRepositoryAlchemy(
        Session(engine)
    )
