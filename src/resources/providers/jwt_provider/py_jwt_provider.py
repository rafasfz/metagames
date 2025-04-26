from dataclasses import dataclass
import jwt
from src.domains.users.entities import UserEntity
from src.resources.providers.jwt_provider.jwt_provider import JWTProvider, Payload
from src.settings import JWT_ALGORITHM, SECRET_KEY


@dataclass
class PyJWTProvider(JWTProvider):

    def generate_token(self, user: UserEntity) -> str:
        payload = {
            "user": user.model_dump(mode="json"),
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token

    def verify_token(self, token: str) -> Payload | None:
        try:
            return Payload(
                **jwt.decode(
                    token,
                    SECRET_KEY,
                    algorithms=[JWT_ALGORITHM],
                )
            )
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
