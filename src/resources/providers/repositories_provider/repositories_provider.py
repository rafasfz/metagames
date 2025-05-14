from abc import ABC
from dataclasses import dataclass

from src.domains.games.repositories.platform_repository import PlatformRepository
from src.domains.users.repositories.user_repository import UserRepository


@dataclass
class RepositoriesProvider(ABC):
    user_repository: UserRepository
    platform_repository: PlatformRepository
