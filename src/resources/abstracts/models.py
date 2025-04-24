from datetime import datetime
from sqlalchemy import UUID
from src.infrastructure.db import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class AbstractModel(Base):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column("created_at", nullable=False)
    updated_at: Mapped[datetime] = mapped_column("updated_at", nullable=False)
