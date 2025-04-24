from abc import ABC, abstractmethod

from src.domains.users.entities import UserEntity, UserWithPasswordHash
from src.domains.users.repositories.user_repository import UserRepository
from src.domains.users.models import UserModel


class UserRepositoryORM(UserRepository):

    def create_user(self, user: UserWithPasswordHash) -> UserEntity:
        user_model = UserModel(**user.model_dump())
        user_model.save()

        user_dict = {
            key: getattr(user_model, key)
            for key in UserEntity.__annotations__.keys()
            if hasattr(user_model, key)
        }

        user_dict.pop("password_hash")

        return UserEntity(**user_dict)
