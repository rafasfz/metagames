from dataclasses import dataclass
from sqlalchemy.orm import Session
from src.infrastructure.db import engine
from src.domains.users.entities import UserEntity, UserToSave
from src.domains.users.repositories.user_repository import UserRepository
from src.domains.users.models import UserModel


class UserRepositoryORM(UserRepository):
    session: Session

    def __init__(self):
        self.session = Session(engine)

    def create_user(self, user: UserToSave) -> UserEntity:
        user_model = UserModel(**user.model_dump())

        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)

        user_dict = {
            key: getattr(user_model, key)
            for key in UserEntity.model_fields.keys()
            if hasattr(user_model, key)
        }

        return UserEntity(**user_dict)
