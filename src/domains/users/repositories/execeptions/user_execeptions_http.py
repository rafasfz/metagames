from fastapi import HTTPException
from src.domains.users.repositories.execeptions.user_execeptions import UserExceptions


class UserExceptionsHTTP(UserExceptions):

    def user_already_exists(self, field: str) -> Exception:
        raise HTTPException(
            status_code=400,
            detail=f"User with {field} already exists",
        )
