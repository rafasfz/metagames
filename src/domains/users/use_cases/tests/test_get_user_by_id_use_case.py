from uuid import UUID
from fastapi import HTTPException
import pytest
from src.domains.users.entities import UserEntity, UserInputs, UserToSave
from src.domains.users.use_cases.get_user_by_id_use_case import (
    GetUserByIdUseCase,
    InputsGetUserByIdUseCase,
)
from src.resources.providers.exceptions_provider.exceptions_provider_http import (
    ExceptionsProviderHTTP,
)
from src.resources.providers.repositories_provider.repositories_provider_orm import (
    RepositoriesProviderORM,
)


@pytest.fixture
def user_on_db(
    repositories_provider_orm: RepositoriesProviderORM,
    user_inputs: UserInputs,
) -> UserEntity:

    user = repositories_provider_orm.user_repository.create_user(
        user=UserToSave(
            **user_inputs.model_dump(exclude={"password"}),
            password_hash="hashed_password",
        )
    )
    return user


def test_get_user_by_id_use_case(
    repositories_provider_orm: RepositoriesProviderORM,
    user_on_db: UserEntity,
):
    user = (
        GetUserByIdUseCase(
            repositories_provider=repositories_provider_orm,
            exceptions_provider=ExceptionsProviderHTTP(),
        )
        .execute(inputs=InputsGetUserByIdUseCase(id=user_on_db.id))
        .user
    )

    assert user_on_db.id == user.id
    assert user_on_db.email == user.email
    assert user_on_db.username == user.username


def test_error_get_user_not_existis_by_id(
    repositories_provider_orm: RepositoriesProviderORM,
):
    with pytest.raises(HTTPException) as excinfo:
        GetUserByIdUseCase(
            repositories_provider=repositories_provider_orm,
            exceptions_provider=ExceptionsProviderHTTP(),
        ).execute(
            inputs=InputsGetUserByIdUseCase(
                id=UUID("12345678-1234-5678-1234-567812345678")
            )
        )

    assert excinfo.value.status_code == 404
