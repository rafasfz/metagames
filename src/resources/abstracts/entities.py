from datetime import datetime
from typing import TypeVar
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from sqlalchemy.orm import DeclarativeMeta

TypeEntity = TypeVar("TypeEntity", bound="AbstractEntity")


class AbstractEntity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def transform_model_to_entity(
        cls: type[TypeEntity],
        model: DeclarativeMeta,
    ) -> TypeEntity:
        entity_dict = {
            key: getattr(model, key)
            for key in cls.model_fields.keys()
            if hasattr(model, key)
        }
        return cls(**entity_dict)
