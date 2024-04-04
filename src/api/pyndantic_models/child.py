import datetime
import uuid
from typing import Optional
from uuid import UUID

import pydantic

from api.pyndantic_models.base_model import UpdatableBaseModel


class ChildIn(UpdatableBaseModel):
    name: Optional[str] = pydantic.Field(default=None)
    surname: Optional[str] = pydantic.Field(default=None)
    patronymic: Optional[str] = pydantic.Field(default=None)
    dob: Optional[datetime.datetime] = pydantic.Field(default=None)


class ChildModel(ChildIn):
    id: UUID = pydantic.Field(default_factory=uuid.uuid4, frozen=True)
