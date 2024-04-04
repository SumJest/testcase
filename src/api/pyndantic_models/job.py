import datetime
import decimal
import uuid
from enum import Enum
from typing import Optional, Annotated, Any
from uuid import UUID

import pydantic

from .address import AddressModel, AddressIn
from .base_model import UpdatableBaseModel


class JobType(Enum):
    main = "main"
    part_time = "part-time"


class JobIn(UpdatableBaseModel):
    type: Optional[JobType] = pydantic.Field(default=None)
    dateEmp: Optional[datetime.datetime] = pydantic.Field(default=None)
    dateDismissal: Optional[datetime.datetime] = pydantic.Field(default=None)
    monIncome: Annotated[decimal.Decimal, pydantic.Field(decimal_places=2)] | None = None
    tin: Optional[str] = pydantic.Field(default=None)
    factAddress: Optional[AddressIn] = pydantic.Field(default=None)
    jurAddress: Optional[AddressIn] = pydantic.Field(default=None)
    phoneNumber: Optional[str] = pydantic.Field(default=None)


class JobModel(JobIn):
    id: UUID = pydantic.Field(default_factory=uuid.uuid4, frozen=True)
    factAddress: Optional[AddressModel] = pydantic.Field(default=None)
    jurAddress: Optional[AddressModel] = pydantic.Field(default=None)
    createdAt: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now, frozen=True)
    updatedAt: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now, frozen=True)
