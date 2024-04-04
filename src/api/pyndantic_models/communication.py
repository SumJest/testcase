import uuid
from enum import Enum
from uuid import UUID

import pydantic

from api.pyndantic_models.base_model import UpdatableBaseModel


class CommunicationType(Enum):
    email = "email"
    phone = "phone"


class CommunicationIn(UpdatableBaseModel):
    type: CommunicationType = pydantic.Field(...)
    value: str = pydantic.Field(...)


class CommunicationModel(CommunicationIn):
    id: UUID = pydantic.Field(default_factory=uuid.uuid4, frozen=True)
