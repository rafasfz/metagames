from dataclasses import dataclass
from pydantic import BaseModel

from src.domains.games.entities import PlatformData, PlatformEntity
from src.domains.games.repositories.platform_repository import PlatformRepository
from src.resources.abstracts.use_case import AbstractUseCase
from src.resources.providers.repositories_provider.repositories_provider import (
    RepositoriesProvider,
)


class InputsCreatePlatformUseCase(BaseModel):
    platform: PlatformData


class OutputsCreatePlatformUseCase(BaseModel):
    platform: PlatformEntity


@dataclass(kw_only=True)
class CreatePlatformUseCase(
    AbstractUseCase[InputsCreatePlatformUseCase, OutputsCreatePlatformUseCase]
):
    repositories_provider_orm: RepositoriesProvider

    def _execute(
        self,
        inputs: InputsCreatePlatformUseCase,
    ) -> OutputsCreatePlatformUseCase:
        platform = self.repositories_provider_orm.platform_repository.create_platform(
            platform_data=PlatformEntity(**inputs.platform.model_dump()),
        )

        return OutputsCreatePlatformUseCase(platform=platform)
