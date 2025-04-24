from dataclasses import dataclass
from pydantic import BaseModel, Field
import bcrypt

from src.domains.users.entities import UserData, UserEntity, UserToSave
from src.domains.users.repositories.execeptions.user_execeptions import UserExceptions
from src.domains.users.repositories.user_repository import UserRepository


class UserInputs(UserData):
    password: str = Field(min_length=8, max_length=128)


class InputsCreateUserUseCase(BaseModel):
    user: UserInputs = Field()


class OutputsCreateUserUseCase(BaseModel):
    user: UserEntity = Field()


# TODO: VALIDAR SE USUARIO JÁ EXISTE E DISPIRAR ERRO COM STATUS CODE CORRETO


@dataclass
class CreateUserUseCase:
    user_repository: UserRepository
    user_exceptions: UserExceptions

    def execute(self, inputs: InputsCreateUserUseCase) -> OutputsCreateUserUseCase:
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

        password_hash = bcrypt.hashpw(
            inputs.user.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user_with_password_hash = UserToSave(
            **inputs.user.model_dump(exclude={"password"}),
            password_hash=password_hash,
        )

        user = self.user_repository.create_user(user_with_password_hash)

        return OutputsCreateUserUseCase(user=user)
