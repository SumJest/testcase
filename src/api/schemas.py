import uuid
from typing import Optional
from uuid import UUID

import ninja
import pydantic

from api.models import Client as ClientDB
from api.pyndantic_models import (ChildIn, CommunicationIn, AddressIn, CommunicationType, JobIn,
                                  PassportIn, JobType, ClientIn)


class PaginationResponseBody(ninja.Schema):
    limit: int = ninja.Field()
    page: int = ninja.Field()
    total: int = ninja.Field()
    data: list[ninja.Schema] = ninja.Field()


class OutClientWithSpouse(ninja.ModelSchema):
    class Meta:
        model = ClientDB
        exclude = ['deleted_at', 'restored_at']


class InPassport(ninja.Schema, PassportIn):
    pass


class InAddress(ninja.Schema, AddressIn):
    pass


class InJob(ninja.Schema, JobIn):
    factAddress: Optional[InAddress] = pydantic.Field(default=None)
    jurAddress: Optional[InAddress] = pydantic.Field(default=None)


class InChild(ninja.Schema, ChildIn):
    pass


class InCommunication(ninja.Schema, CommunicationIn):
    pass


class InClient(ninja.Schema, ClientIn):
    passport: Optional[InPassport] = pydantic.Field(default=None)
    livingAddress: Optional[InAddress] = pydantic.Field(default=None)
    regAddress: Optional[InAddress] = pydantic.Field(default=None)
    children: Optional[InChild] = pydantic.Field(default=[])

    jobs: Optional[list[InJob]] = pydantic.Field(default=[])
    communications: Optional[list[InCommunication]] = pydantic.Field(default=[])
    pass


class InClientWithSpouse(InClient):
    passport: Optional[InPassport] = pydantic.Field(default=None)
    livingAddress: Optional[InAddress] = pydantic.Field(default=None)
    regAddress: Optional[InAddress] = pydantic.Field(default=None)
    children: Optional[InChild] = pydantic.Field(default=[])

    jobs: Optional[list[InJob]] = pydantic.Field(default=[])
    communications: Optional[list[InCommunication]] = pydantic.Field(default=[])

    spouse: InClient = pydantic.Field(default=None)


class NoContent(ninja.Schema):
    pass
