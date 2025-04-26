from dataclasses import dataclass
from pydantic import BaseModel, Field

from src.domains.users.entities import UserEntity, UserInputs, UserRole, UserToSave
from src.domains.users.exceptions.user_exceptions import UserExceptions
from src.domains.users.repositories.user_repository import UserRepository
from src.resources.abstracts.use_case import AbstractUseCase
from src.resources.providers.password_hasher.password_hasher import PasswordHasher


class InputsCreateUserUseCase(BaseModel):
    user: UserInputs = Field()


class OutputsCreateUserUseCase(BaseModel):
    user: UserEntity = Field()


@dataclass(kw_only=True)
class CreateUserUseCase(
    AbstractUseCase[InputsCreateUserUseCase, OutputsCreateUserUseCase]
):
    user_repository: UserRepository
    password_hasher: PasswordHasher

    def _validate(self, inputs: InputsCreateUserUseCase) -> None:
        is_user_email_already_exists = self.user_repository.get_user_by_email(
            email=inputs.user.email
        )

        if is_user_email_already_exists:
            raise self.exceptions_provider.user_exceptions.user_already_exists(
                field="email"
            )

        is_username_already_exists = self.user_repository.get_user_by_username(
            username=inputs.user.username
        )

        if is_username_already_exists:
            raise self.exceptions_provider.user_exceptions.user_already_exists(
                field="username"
            )

    def _execute(self, inputs: InputsCreateUserUseCase) -> OutputsCreateUserUseCase:
        self._validate(inputs)

        password_hash = self.password_hasher.hash(inputs.user.password)

        user_with_password_hash = UserToSave(
            **inputs.user.model_dump(exclude={"password"}),
            password_hash=password_hash,
        )

        if not self.user or not self.user.is_admin():
            user_with_password_hash.role = UserRole.USER

        user = self.user_repository.create_user(user_with_password_hash)

        return OutputsCreateUserUseCase(user=user)
