from dataclasses import dataclass
from pydantic import BaseModel

from src.domains.users.entities import UserEntity
from src.resources.providers.jwt_provider.jwt_provider import JWTProvider


class InputsGetUserIfAuthenticatedUseCase(BaseModel):
    token: str


class OutputsGetUserIfAuthenticatedUseCase(BaseModel):
    user: UserEntity | None


@dataclass
class GetUserIfAuthenticatedUseCase:
    jwt_provider: JWTProvider

    def execute(
        self,
        inputs: InputsGetUserIfAuthenticatedUseCase,
    ) -> OutputsGetUserIfAuthenticatedUseCase:
        payload = self.jwt_provider.verify_token(inputs.token)

        if payload is None:
            return OutputsGetUserIfAuthenticatedUseCase(user=None)

        user = payload.user
        return OutputsGetUserIfAuthenticatedUseCase(user=user)
