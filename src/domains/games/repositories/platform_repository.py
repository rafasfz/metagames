from abc import ABC, abstractmethod
from uuid import UUID

from src.domains.games.entities import PlatformEntity


class PlatformRepository(ABC):

    @abstractmethod
    def create_platform(self, platform_data: PlatformEntity) -> PlatformEntity:
        raise NotImplementedError("Method not implemented")
