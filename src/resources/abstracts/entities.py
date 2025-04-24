from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, model_validator


class AbstractEntity(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        validate_assignment = True

    # @model_validator(mode="after")
    # def number_validator(cls, values):
    #     values["updated_at"] = datetime.now()
    #     return values
