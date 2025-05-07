from typing import Callable
from src.domains.authentication.use_cases.get_user_if_authenticated_use_case import (
    GetUserIfAuthenticatedUseCase,
    InputsGetUserIfAuthenticatedUseCase,
)
from src.domains.authentication.use_cases.login_use_case import (
    OutputsLoginUseCase,
    UserLoginInputs,
)
from src.domains.users.entities import UserEntity, UserInputs


def test_get_user_authenticated_use_case(
    registred_user: UserEntity,
    user_inputs: UserInputs,
    login_user: Callable[[UserLoginInputs], OutputsLoginUseCase],
    get_user_if_authenticated_use_case: GetUserIfAuthenticatedUseCase,
):
    login_inputs = UserLoginInputs(
        username=user_inputs.username,
        password=user_inputs.password,
    )

    outputs_login = login_user(login_inputs)

    outputs = get_user_if_authenticated_use_case.execute(
        inputs=InputsGetUserIfAuthenticatedUseCase(
            token=outputs_login.access_token,
        ),
    )

    assert outputs.user == registred_user


def test_not_get_user_authenticated_use_case(
    get_user_if_authenticated_use_case: GetUserIfAuthenticatedUseCase,
):
    outputs = get_user_if_authenticated_use_case.execute(
        inputs=InputsGetUserIfAuthenticatedUseCase(
            token="",
        ),
    )

    assert outputs.user is None
