from dataclasses import dataclass
from sqlalchemy.orm import Session
from src.infrastructure.db import engine
from src.domains.users.entities import UserEntity, UserToSave
from src.domains.users.repositories.user_repository import UserRepository
from src.domains.users.models import UserModel
from src.resources.abstracts.entities import transform_model_to_entity


class UserRepositoryORM(UserRepository):
    session: Session

    def __init__(self):
        self.session = Session(engine)

    def create_user(self, user: UserToSave) -> UserEntity:
        user_model = UserModel(**user.model_dump())

        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)

        user_entity = transform_model_to_entity(user_model, UserEntity)

        return user_entity

    def get_user_by_email(self, email: str) -> UserEntity | None:
        user_model = self.session.query(UserModel).filter_by(email=email).first()

        if not user_model:
            return None

        user_entity = transform_model_to_entity(user_model, UserEntity)

        return user_entity

    def get_user_by_username(self, username: str) -> UserEntity | None:
        user_model = self.session.query(UserModel).filter_by(username=username).first()

        if not user_model:
            return None

        user_entity = transform_model_to_entity(user_model, UserEntity)

        return user_entity

    def get_user_by_id(self, id: str) -> UserEntity | None:
        user_model = self.session.query(UserModel).filter_by(id=id).first()

        if not user_model:
            return None

        user_entity = transform_model_to_entity(user_model, UserEntity)

        return user_entity
