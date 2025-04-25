from dataclasses import dataclass
from uuid import UUID
from pydantic import BaseModel, Field

from src.domains.users.entities import UserEntity
from src.domains.users.exceptions.user_exceptions import UserExceptions
from src.domains.users.repositories.user_repository import UserRepository


class InputsGetUserByIdUseCase(BaseModel):
    id: UUID = Field()


class OutputsGetUserByIdUseCase(BaseModel):
    user: UserEntity = Field()


@dataclass
class GetUserByIdUseCase:
    user_repository: UserRepository
    user_exceptions: UserExceptions

    def execute(self, inputs: InputsGetUserByIdUseCase) -> OutputsGetUserByIdUseCase:
        user = self.user_repository.get_user_by_id(id=inputs.id)

        if not user:
            raise self.user_exceptions.user_not_found(id=inputs.id)

        return OutputsGetUserByIdUseCase(user=user)
