from dataclasses import dataclass
from typing import cast
from pydantic import BaseModel

from src.domains.authentication.exceptions.authentication_exceptions import (
    AuthenticationExceptions,
)
from src.domains.users.entities import UserEntity
from src.domains.users.repositories.user_repository import UserRepository
from src.resources.providers.jwt_provider.jwt_provider import JWTProvider
from src.resources.providers.password_hasher.password_hasher import PasswordHasher


class UserLoginInputs(BaseModel):
    username: str
    password: str


class InputsLoginUseCase(BaseModel):
    user: UserLoginInputs


class OutputsLoginUseCase(BaseModel):
    access_token: str
    user: UserEntity


@dataclass
class LoginUseCase:
    user_repository: UserRepository
    jwt_provider: JWTProvider
    password_hasher: PasswordHasher
    authentication_exceptions: AuthenticationExceptions

    def execute(self, inputs: InputsLoginUseCase) -> OutputsLoginUseCase:

        self._validate(inputs=inputs)

        user = cast(
            UserEntity,
            self.user_repository.get_user_by_username(username=inputs.user.username),
        )

        access_token = self.jwt_provider.generate_token(user=user)

        return OutputsLoginUseCase(
            access_token=access_token,
            user=user,
        )

    def _validate(self, inputs: InputsLoginUseCase) -> None:
        password_hash = self.user_repository.get_user_password_hash_by_username(
            username=inputs.user.username
        )

        if not password_hash:
            raise self.authentication_exceptions.invalid_credentials()

        is_password_valid = self.password_hasher.verify(
            plain_password=inputs.user.password, hashed_password=password_hash
        )

        if not is_password_valid:
            raise self.authentication_exceptions.invalid_credentials()
