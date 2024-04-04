import decimal
import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, Annotated
from uuid import UUID

from api.pyndantic_models import ChildIn, PassportModel, AddressModel, JobModel, ChildModel, CommunicationModel, \
    PassportIn, AddressIn, JobIn, CommunicationIn
from api.pyndantic_models.base_model import UpdatableBaseModel
import pydantic


class EducationType(Enum):
    secondary = "secondary"
    secondarySpecial = "secondarySpecial"
    incompleteHigher = "incompleteHigher"
    higher = "higher"
    twoOrMoreHigher = "twoOrMoreHigher"
    academicDegree = "academicDegree"


class ClientIn(UpdatableBaseModel):
    children: list[ChildIn] = pydantic.Field(default=[])

    documentIds: list[UUID] = pydantic.Field(default=[])

    passport: PassportIn = pydantic.Field(null=True)

    livingAddress: AddressIn = pydantic.Field(null=True)
    regAddress: AddressIn = pydantic.Field(null=True)

    jobs: list[JobIn] = pydantic.Field(default=[])

    curWorkExp: Optional[int] = pydantic.Field(default=None)
    typeEducation: EducationType = pydantic.Field(...)
    monIncome: Annotated[decimal.Decimal, pydantic.Field(decimal_places=2)] | None = None
    monExpenses: Annotated[decimal.Decimal, pydantic.Field(decimal_places=2)] | None = None
    communications: list[CommunicationIn] = pydantic.Field(...)

class ClientModel(ClientIn):
    id: UUID = pydantic.Field(default_factory=uuid.uuid4, frozen=True)

    children: list[ChildModel] = pydantic.Field(default=[])

    passport: PassportModel = pydantic.Field(null=True)

    livingAddress: AddressModel = pydantic.Field(null=True)
    regAddress: AddressModel = pydantic.Field(null=True)

    jobs: list[JobModel] = pydantic.Field(default=[])
    communications: list[CommunicationModel] = pydantic.Field(...)

    name: Optional[str] = pydantic.Field(default=None)
    surname: Optional[str] = pydantic.Field(default=None)
    patronymic: Optional[str] = pydantic.Field(default=None)
    dob: datetime = pydantic.Field(...)

    createdAt: datetime = pydantic.Field(default_factory=datetime.now, frozen=True)
    updatedAt: datetime = pydantic.Field(default_factory=datetime.now, frozen=True)
