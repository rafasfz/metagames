from dataclasses import dataclass
from pydantic import BaseModel, Field

from src.domains.users.entities import UserData, UserEntity, UserToSave
from src.domains.users.repositories.execeptions.user_execeptions import UserExceptions
from src.domains.users.repositories.user_repository import UserRepository
from src.resources.password_hasher.password_hasher import PasswordHasher


class UserInputs(UserData):
    password: str = Field(min_length=8, max_length=128)


class InputsCreateUserUseCase(BaseModel):
    user: UserInputs = Field()


class OutputsCreateUserUseCase(BaseModel):
    user: UserEntity = Field()


@dataclass
class CreateUserUseCase:
    user_repository: UserRepository
    user_exceptions: UserExceptions
    password_hasher: PasswordHasher

    def validate(self, inputs: InputsCreateUserUseCase) -> None:
        is_user_email_already_exists = self.user_repository.get_user_by_email(
            email=inputs.user.email
        )

        if is_user_email_already_exists:
            raise self.user_exceptions.user_already_exists(field="email")

        is_username_already_exists = self.user_repository.get_user_by_username(
            username=inputs.user.username
        )

        if is_username_already_exists:
            raise self.user_exceptions.user_already_exists(field="username")

    def execute(self, inputs: InputsCreateUserUseCase) -> OutputsCreateUserUseCase:
        self.validate(inputs)

        password_hash = self.password_hasher.hash(inputs.user.password)

        user_with_password_hash = UserToSave(
            **inputs.user.model_dump(exclude={"password"}),
            password_hash=password_hash,
        )

        user = self.user_repository.create_user(user_with_password_hash)

        return OutputsCreateUserUseCase(user=user)
