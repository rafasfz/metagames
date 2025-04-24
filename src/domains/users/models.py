from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from src.resources.abstracts.models import AbstractModel


class UserModel(AbstractModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column("username", nullable=False, unique=True)
    email: Mapped[str] = mapped_column("email", nullable=False, unique=True)
    first_name: Mapped[str] = mapped_column("first_name", nullable=False)
    last_name: Mapped[str] = mapped_column("last_name", nullable=False)
    role: Mapped[str] = mapped_column("role", nullable=False)
    password_hash: Mapped[str] = mapped_column("password_hash", nullable=False)
