from typing import Callable
import pytest
from fastapi import HTTPException
from src.domains.users.entities import UserEntity, UserInputs
from src.domains.authentication.use_cases.login_use_case import (
    LoginUseCase,
    InputsLoginUseCase,
    UserLoginInputs,
    OutputsLoginUseCase,
)
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

INVALID_USERNAME = "usuario_inexistente"
INVALID_PASSWORD = "qualquer_senha"


def test_login_successful(
    registred_user: UserEntity,
    user_inputs: UserInputs,
    login_user: Callable[[UserLoginInputs], OutputsLoginUseCase],
):
    login_inputs = UserLoginInputs(
        username=user_inputs.username,
        password=user_inputs.password,
    )

    outputs = login_user(login_inputs)

    assert outputs.access_token is not None
    assert outputs.user == registred_user


def test_login_invalid_username(
    login_user: Callable[[UserLoginInputs], OutputsLoginUseCase],
):
    login_inputs = UserLoginInputs(
        username=INVALID_USERNAME,
        password=INVALID_PASSWORD,
    )

    with pytest.raises(HTTPException) as http_exception:
        login_user(login_inputs)

    assert http_exception.value.status_code == 401


def test_login_invalid_password(
    registred_user: UserEntity,
    login_user: Callable[[UserLoginInputs], OutputsLoginUseCase],
):
    login_inputs = UserLoginInputs(
        username=registred_user.username,
        password=INVALID_PASSWORD,
    )

    with pytest.raises(HTTPException) as http_exception:
        login_user(login_inputs)

    assert http_exception.value.status_code == 401


def test_jwt_token_valid_generation(
    registred_user: UserEntity,
    user_inputs: UserInputs,
    repositories_provider_orm: RepositoriesProviderORM,
):

    login_inputs = UserLoginInputs(
        username=registred_user.username,
        password=user_inputs.password,
    )

    outputs = LoginUseCase(
        repositories_provider=repositories_provider_orm,
        jwt_provider=PyJWTProvider(),
        password_hasher=PasswordHasherBCrypt(),
        exceptions_provider=ExceptionsProviderHTTP(),
    ).execute(InputsLoginUseCase(user=login_inputs))

    valid_token = PyJWTProvider().verify_token(token=outputs.access_token)

    assert outputs.access_token is not None
    assert isinstance(outputs.access_token, str)
    assert valid_token is not None
