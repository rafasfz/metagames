from datetime import datetime
from typing import TypeVar
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, model_validator
from sqlalchemy.orm import DeclarativeMeta

TypeEntity = TypeVar("TypeEntity", bound="AbstractEntity")


class AbstractEntity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


def transform_model_to_entity(
    model: DeclarativeMeta, entity: type[TypeEntity]
) -> TypeEntity:
    entity_dict = {
        key: getattr(model, key)
        for key in entity.model_fields.keys()
        if hasattr(model, key)
    }
    return entity(**entity_dict)
