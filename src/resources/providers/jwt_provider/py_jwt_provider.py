import jwt
from datetime import timedelta
from typing import Optional
from src.domains.users.entities import UserEntity
from src.resources.providers.jwt_provider.jwt_provider import JWTProvider, Payload
from src.settings import JWT_ALGORITHM, SECRET_KEY


class PyJWTProvider(JWTProvider):
    def generate_token(
        self, user: UserEntity, expires_in: Optional[timedelta] = None
    ) -> str:
        payload = {
            "user": user.model_dump_json(),
            "exp": None,
        }

        if expires_in:
            payload["exp"] = int(expires_in.total_seconds())

        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        return token

    # TODO: UPDATE EXCEPTION FOR INVERSION DEPENDECY WITH FASTAPI ERRORS
    def verify_token(self, token: str) -> Payload:
        try:
            return jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado")
        except jwt.InvalidTokenError:
            raise ValueError("Token inválido")
