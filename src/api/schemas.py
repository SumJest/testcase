from typing import Optional
from uuid import UUID

import ninja

from api.models import Client, Job, Communication, Child, Address, Passport


class InAddress(ninja.ModelSchema):
    class Meta:
        model = Address
        exclude = ["id", "createdAt", "updatedAt"]


class InChild(ninja.ModelSchema):
    class Meta:
        model = Child
        exclude = ["id", "client"]


class PaginationResponseBody(ninja.Schema):
    limit: int = ninja.Field()
    page: int = ninja.Field()
    total: int = ninja.Field()
    data: list[ninja.Schema] = ninja.Field()


class ExceptionSchema(ninja.Schema):
    status: int
    code: str


class ValidationExceptions(ninja.Schema):
    field: str = ninja.Field()
    rule: str = ninja.Field()
    message: str = ninja.Field()


class ValidationErrorSchema(ExceptionSchema):
    exceptions: list[ValidationExceptions] = []


class InCommunication(ninja.ModelSchema):
    class Meta:
        model = Communication
        exclude = ["id", "client"]


class InJob(ninja.ModelSchema):
    factAddress: Optional[InAddress] = ninja.Field(default=None)
    jurAddress: Optional[InAddress] = ninja.Field(default=None)

    class Meta:
        model = Job
        exclude = ["id", "client", "createdAt", "updatedAt"]


class InPassport(ninja.ModelSchema):
    class Meta:
        model = Passport
        exclude = ["id", "createdAt", "updatedAt"]


class InClientSchema(ninja.ModelSchema):
    passport: Optional[InPassport] = ninja.Field(default=None)
    livingAddress: Optional[InAddress] = ninja.Field(default=None)
    regAddress: Optional[InAddress] = ninja.Field(default=None)
    spouse: Optional["InClientSchema"] = ninja.Field(default=None)
    children: list[InChild] = ninja.Field(...)
    jobs: list[InJob] = ninja.Field(...)
    communications: list[InCommunication] = ninja.Field(...)

    class Meta:
        model = Client
        exclude = ["id", "deleted_at", "restored_at", "createdAt", "updatedAt"]


class OutPassport(ninja.ModelSchema):
    class Meta:
        model = Passport
        fields = "__all__"


class OutAddress(ninja.ModelSchema):
    class Meta:
        model = Address
        fields = "__all__"


class OutChild(ninja.ModelSchema):
    class Meta:
        model = Child
        exclude = ["client"]


class OutJob(ninja.ModelSchema):
    factAddress: Optional[OutAddress] = ninja.Field(default=None)
    jurAddress: Optional[OutAddress] = ninja.Field(default=None)

    class Meta:
        model = Job
        exclude = ["client"]


class OutCommunication(ninja.ModelSchema):
    class Meta:
        model = Communication
        exclude = ["client"]


class OutClientWithoutSpouseSchema(ninja.ModelSchema):
    passport: Optional[OutPassport] = ninja.Field(default=None)
    livingAddress: Optional[OutAddress] = ninja.Field(default=None)
    regAddress: Optional[OutAddress] = ninja.Field(default=None)

    children: list[OutChild] = ninja.Field(alias="child_set", default=[])
    jobs: list[OutJob] = ninja.Field(alias='job_set', default=[])
    communications: list[OutCommunication] = ninja.Field(alias='communication_set', default=[])

    class Meta:
        model = Client
        exclude = ['deleted_at', 'restored_at', 'spouse']
        extra = 'allow'


class OutClientSchema(OutClientWithoutSpouseSchema):
    spouse: Optional[OutClientWithoutSpouseSchema] = ninja.Field(default=None)


class PatchAddress(ninja.ModelSchema):
    class Meta:
        model = Address
        exclude = ["id", "createdAt", "updatedAt"]
        fields_optional = "__all__"


class PatchChild(InChild):
    id: Optional[UUID] = None

    class Meta:
        fields_optional = "__all__"


class PatchCommunication(InCommunication):
    id: Optional[UUID] = None

    class Meta:
        fields_optional = "__all__"


class PatchJob(InJob):
    id: Optional[UUID] = None

    class Meta:
        fields_optional = "__all__"


class PatchPassport(ninja.ModelSchema):
    class Meta:
        model = Passport
        exclude = ["id", "createdAt", "updatedAt"]
        fields_optional = "__all__"


class PatchWithoutClientSchema(ninja.ModelSchema):
    passport: Optional[PatchPassport] = None
    livingAddress: Optional[PatchAddress] = None
    regAddress: Optional[PatchAddress] = None
    children: Optional[list[PatchChild]] = None
    jobs: Optional[list[PatchJob]] = None
    communications: Optional[list[PatchCommunication]] = None

    class Meta:
        model = Client
        exclude = ["id", "deleted_at", "restored_at", "createdAt", "updatedAt"]
        fields_optional = "__all__"


class PatchClientSchema(PatchWithoutClientSchema):
    spouse: Optional[PatchWithoutClientSchema] = None
