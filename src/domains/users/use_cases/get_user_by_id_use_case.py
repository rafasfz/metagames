from dataclasses import dataclass
from uuid import UUID
from pydantic import BaseModel, Field

from src.domains.users.entities import UserEntity
from src.domains.users.exceptions.user_exceptions import UserExceptions
from src.domains.users.repositories.user_repository import UserRepository
from src.resources.abstracts.use_case import AbstractUseCase


class InputsGetUserByIdUseCase(BaseModel):
    id: UUID = Field()


class OutputsGetUserByIdUseCase(BaseModel):
    user: UserEntity = Field()


@dataclass(kw_only=True)
class GetUserByIdUseCase(
    AbstractUseCase[InputsGetUserByIdUseCase, OutputsGetUserByIdUseCase]
):
    user_repository: UserRepository

    def _execute(self, inputs: InputsGetUserByIdUseCase) -> OutputsGetUserByIdUseCase:
        user = self.user_repository.get_user_by_id(id=inputs.id)

        if not user:
            raise self.exceptions_provider.user_exceptions.user_not_found(id=inputs.id)

        return OutputsGetUserByIdUseCase(user=user)
