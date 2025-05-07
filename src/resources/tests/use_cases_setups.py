from typing import Callable
import pytest

from src.domains.authentication.use_cases.get_user_if_authenticated_use_case import (
    GetUserIfAuthenticatedUseCase,
)
from src.domains.authentication.use_cases.login_use_case import (
    InputsLoginUseCase,
    LoginUseCase,
    OutputsLoginUseCase,
    UserLoginInputs,
)
from src.domains.users.use_cases.create_user_use_case import CreateUserUseCase
from src.resources.providers.exceptions_provider.exceptions_provider_http import (
    ExceptionsProviderHTTP,
)
from src.resources.providers.jwt_provider.py_jwt_provider import PyJWTProvider
from src.resources.providers.password_hasher.password_hasher_bcrypt import (
    PasswordHasherBCrypt,
)
from src.resources.providers.repositories_provider.repositories_provider_orm import (
    RepositoriesProviderORM,
)


@pytest.fixture
def create_user_use_case(
    repositories_provider_orm: RepositoriesProviderORM,
) -> CreateUserUseCase:

    return CreateUserUseCase(
        repositories_provider=repositories_provider_orm,
        password_hasher=PasswordHasherBCrypt(),
        exceptions_provider=ExceptionsProviderHTTP(),
    )


@pytest.fixture
def login_use_case(
    repositories_provider_orm: RepositoriesProviderORM,
) -> LoginUseCase:

    return LoginUseCase(
        repositories_provider=repositories_provider_orm,
        password_hasher=PasswordHasherBCrypt(),
        exceptions_provider=ExceptionsProviderHTTP(),
        jwt_provider=PyJWTProvider(),
    )


@pytest.fixture
def login_user(
    repositories_provider_orm: RepositoriesProviderORM,
) -> Callable[[UserLoginInputs], OutputsLoginUseCase]:
    def _login_user(user_inputs: UserLoginInputs) -> OutputsLoginUseCase:
        inputs = InputsLoginUseCase(user=user_inputs)

        outputs = LoginUseCase(
            repositories_provider=repositories_provider_orm,
            jwt_provider=PyJWTProvider(),
            password_hasher=PasswordHasherBCrypt(),
            exceptions_provider=ExceptionsProviderHTTP(),
        ).execute(inputs=inputs)
        return outputs

    return _login_user


@pytest.fixture
def get_user_if_authenticated_use_case() -> GetUserIfAuthenticatedUseCase:
    return GetUserIfAuthenticatedUseCase(jwt_provider=PyJWTProvider())
