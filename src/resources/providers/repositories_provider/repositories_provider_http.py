from dataclasses import dataclass

from src.domains.users.repositories.user_repository import UserRepository
from src.domains.users.repositories.user_repository_orm import UserRepositoryORM
from src.resources.providers.repositories_provider.repositories_provider import (
    RepositoriesProvider,
)


@dataclass
class RepositoriesProviderORM(RepositoriesProvider):
    user_respository: UserRepositoryORM
