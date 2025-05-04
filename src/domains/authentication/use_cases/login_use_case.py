from dataclasses import dataclass
from typing import cast
from pydantic import BaseModel

from src.domains.users.entities import UserEntity
from src.resources.abstracts.use_case import AbstractUseCase
from src.resources.providers.jwt_provider.jwt_provider import JWTProvider
from src.resources.providers.password_hasher.password_hasher import PasswordHasher
from src.resources.providers.repositories_provider.repositories_provider import (
    RepositoriesProvider,
)


class UserLoginInputs(BaseModel):
    username: str
    password: str


class InputsLoginUseCase(BaseModel):
    user: UserLoginInputs


class OutputsLoginUseCase(BaseModel):
    access_token: str
    user: UserEntity


@dataclass(kw_only=True)
class LoginUseCase(AbstractUseCase[InputsLoginUseCase, OutputsLoginUseCase]):
    repositories_provider: RepositoriesProvider
    jwt_provider: JWTProvider
    password_hasher: PasswordHasher

    def _execute(self, inputs: InputsLoginUseCase) -> OutputsLoginUseCase:

        self._validate(inputs=inputs)

        user = cast(
            UserEntity,
            self.repositories_provider.user_repository.get_user_by_username(
                username=inputs.user.username
            ),
        )

        access_token = self.jwt_provider.generate_token(user=user)

        return OutputsLoginUseCase(
            access_token=access_token,
            user=user,
        )

    def _validate(self, inputs: InputsLoginUseCase) -> None:
        password_hash = self.repositories_provider.user_repository.get_user_password_hash_by_username(
            username=inputs.user.username
        )

        if not password_hash:
            raise self.exceptions_provider.authentication_exceptions.invalid_credentials()

        is_password_valid = self.password_hasher.verify(
            plain_password=inputs.user.password, hashed_password=password_hash
        )

        if not is_password_valid:
            raise self.exceptions_provider.authentication_exceptions.invalid_credentials()
