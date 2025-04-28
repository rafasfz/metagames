from abc import ABC
from dataclasses import dataclass

from src.domains.users.repositories.user_repository import UserRepository


@dataclass
class RepositoriesProvider(ABC):
    user_respository: UserRepository
