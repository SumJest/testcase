import datetime
import uuid
from enum import Enum
from typing import Any
from uuid import UUID

import pydantic

from api.pyndantic_models.base_model import UpdatableBaseModel


class PassportIn(UpdatableBaseModel):
    series: str = pydantic.Field(...)
    number: str = pydantic.Field(...)
    giver: str = pydantic.Field(...)
    dateIssued: datetime.datetime = pydantic.Field(...)


class PassportModel(PassportIn):
    id: UUID = pydantic.Field(default_factory=uuid.uuid4, frozen=True)

    createdAt: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now, frozen=True)
    updatedAt: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now, frozen=True)
