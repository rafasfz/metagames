from dataclasses import dataclass
import jwt
from src.domains.authentication.exceptions.authentication_exceptions import (
    AuthenticationExceptions,
)
from src.domains.users.entities import UserEntity
from src.resources.providers.jwt_provider.jwt_provider import JWTProvider, Payload
from src.settings import JWT_ALGORITHM, SECRET_KEY


@dataclass
class PyJWTProvider(JWTProvider):
    authentication_exceptions: AuthenticationExceptions

    def generate_token(self, user: UserEntity) -> str:
        payload = {
            "user": user.model_dump(mode="json"),
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token

    def verify_token(self, token: str) -> Payload:
        try:
            return jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            raise self.authentication_exceptions.invalid_token()
        except jwt.InvalidTokenError:
            raise self.authentication_exceptions.invalid_token()
