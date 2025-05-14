from src.domains.games.entities import PlatformData
from src.domains.games.use_cases.create_platform_use_case import (
    CreatePlatformUseCase,
    InputsCreatePlatformUseCase,
)
from src.domains.users.entities import UserEntity


def test_create_platform_use_case(create_platform_use_case: CreatePlatformUseCase):
    inputs = InputsCreatePlatformUseCase(
        platform=PlatformData(
            name="Video Game",
        )
    )

    platform = create_platform_use_case.execute(
        inputs=inputs,
    ).platform

    assert platform.name == inputs.platform.name
