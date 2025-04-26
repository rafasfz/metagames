from abc import abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar, cast

from src.domains.users.entities import UserEntity
from src.resources.providers.exceptions_provider.exceptions_provider import (
    ExceptionsProvider,
)


InputsUseCase = TypeVar("InputsUseCase")
OutputsUseCase = TypeVar("OutputsUseCase")


@dataclass
class AbstractUseCase(Generic[InputsUseCase, OutputsUseCase]):
    exceptions_provider: ExceptionsProvider

    user: UserEntity | None = None
    is_nedded_authentication: bool = False
    is_nedded_be_admin: bool = False
    is_nedded_be_enterprise: bool = False

    def execute(self, inputs: InputsUseCase) -> OutputsUseCase:
        if self.is_nedded_authentication and not self.user:
            raise self.exceptions_provider.authentication_exceptions.unauthorized()

        self.user = cast(UserEntity, self.user)

        if self.is_nedded_be_admin and not self.user.is_admin():
            raise self.exceptions_provider.authentication_exceptions.forbidden()

        if self.is_nedded_be_enterprise and not self.user.is_company():
            raise self.exceptions_provider.authentication_exceptions.forbidden()

        outputs = self._execute(inputs)

        return outputs

    @abstractmethod
    def _execute(self, inputs: InputsUseCase) -> OutputsUseCase:
        raise NotImplementedError("Method not implemented")
