import datetime
import typing
import uuid
from uuid import UUID

import pydantic

from api.pyndantic_models.base_model import UpdatableBaseModel


class AddressIn(UpdatableBaseModel):
    zipCode: str = pydantic.Field(default=None)
    country: str = pydantic.Field(default=None)
    region: str = pydantic.Field(default=None)
    city: str = pydantic.Field(default=None)
    apartment: str = pydantic.Field(default=None)


class AddressModel(AddressIn):
    id: UUID = pydantic.Field(default_factory=uuid.uuid4, frozen=True)

    createdAt: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now, frozen=True)
    updatedAt: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now, frozen=True)
