from dataclasses import dataclass
from pydantic import BaseModel, Field

from src.domains.users.entities import UserEntity, UserInputs, UserRole, UserToSave
from src.resources.abstracts.use_case import AbstractUseCase
from src.resources.providers.password_hasher.password_hasher import PasswordHasher
from src.resources.providers.repositories_provider.repositories_provider import (
    RepositoriesProvider,
)


class InputsCreateUserUseCase(BaseModel):
    user: UserInputs = Field()


class OutputsCreateUserUseCase(BaseModel):
    user: UserEntity = Field()


@dataclass(kw_only=True)
class CreateUserUseCase(
    AbstractUseCase[InputsCreateUserUseCase, OutputsCreateUserUseCase]
):
    repositories_provider: RepositoriesProvider
    password_hasher: PasswordHasher

    def _execute(self, inputs: InputsCreateUserUseCase) -> OutputsCreateUserUseCase:
        self._validate(inputs)

        password_hash = self.password_hasher.hash(inputs.user.password)

        user_with_password_hash = UserToSave(
            **inputs.user.model_dump(exclude={"password"}),
            password_hash=password_hash,
        )

        if not self.authenticated_user or not self.authenticated_user.is_admin():
            user_with_password_hash.role = UserRole.USER

        user = self.repositories_provider.user_repository.create_user(
            user_with_password_hash
        )

        return OutputsCreateUserUseCase(user=user)

    def _validate(self, inputs: InputsCreateUserUseCase) -> None:
        is_user_email_already_exists = (
            self.repositories_provider.user_repository.get_user_by_email(
                email=inputs.user.email
            )
        )

        if is_user_email_already_exists:
            raise self.exceptions_provider.user_exceptions.user_already_exists(
                field="email"
            )

        is_username_already_exists = (
            self.repositories_provider.user_repository.get_user_by_username(
                username=inputs.user.username
            )
        )

        if is_username_already_exists:
            raise self.exceptions_provider.user_exceptions.user_already_exists(
                field="username"
            )
