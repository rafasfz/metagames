from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.domains.authentication.routes import get_user_if_authenticated
from src.domains.games.use_cases.create_platform_use_case import (
    CreatePlatformUseCase,
    InputsCreatePlatformUseCase,
    OutputsCreatePlatformUseCase,
)
from src.domains.users.entities import UserEntity
from src.resources.providers.exceptions_provider.exceptions_provider_http import (
    ExceptionsProviderHTTP,
)
from src.resources.providers.repositories_provider.repositories_provider_orm import (
    RepositoriesProviderORM,
)


users_router = APIRouter(
    prefix="/platform",
)


@users_router.post("/", status_code=status.HTTP_201_CREATED)
def create_platform(
    inputs: InputsCreatePlatformUseCase,
    user: Annotated[UserEntity | None, Depends(get_user_if_authenticated)],
) -> OutputsCreatePlatformUseCase:

    outputs = CreatePlatformUseCase(
        authenticated_user=user,
        repositories_provider_orm=RepositoriesProviderORM(),
        is_nedded_be_admin=True,
        exceptions_provider=ExceptionsProviderHTTP(),
    ).execute(inputs=inputs)

    return outputs
