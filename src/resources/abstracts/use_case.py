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

    authenticated_user: UserEntity | None = None
    is_nedded_authentication: bool = False
    is_nedded_be_admin: bool = False
    is_nedded_be_enterprise: bool = False

    def execute(self, inputs: InputsUseCase) -> OutputsUseCase:
        if (
            self.is_nedded_authentication
            or self.is_nedded_be_admin
            or self.is_nedded_be_enterprise
        ) and not self.authenticated_user:
            raise self.exceptions_provider.authentication_exceptions.unauthorized()

        self.authenticated_user = cast(UserEntity, self.authenticated_user)

        if self.is_nedded_be_admin and not self.authenticated_user.is_admin():
            raise self.exceptions_provider.authentication_exceptions.forbidden()

        if self.is_nedded_be_enterprise and not self.authenticated_user.is_company():
            raise self.exceptions_provider.authentication_exceptions.forbidden()

        outputs = self._execute(inputs)

        return outputs

    @abstractmethod
    def _execute(self, inputs: InputsUseCase) -> OutputsUseCase:
        raise NotImplementedError("Method not implemented")
