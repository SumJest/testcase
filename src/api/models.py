import json
import typing
import uuid

from django.db import models

from api.pyndantic_models import ChildModel, PassportModel
from api.pyndantic_models import CommunicationModel
from api.pyndantic_models import AddressModel
from api.pyndantic_models import JobModel
from api.pyndantic_models import ClientModel
from api.services.json_uuid import UUIDJsonEncoder
from django_softdelete.models import SoftDeleteModel
from django_pydantic_field import SchemaField


# Create your models here.

class EducationType(models.TextChoices):
    secondary = "secondary", "Среднее"
    secondarySpecial = "secondarySpecial", "Среднее специальное"
    incompleteHigher = "incompleteHigher", "Незаконченное высшее"
    higher = "higher", "Высшее"
    twoOrMoreHigher = "twoOrMoreHigher", "Два и более высших образований"
    academicDegree = "academicDegree", "Академическая степень"


class ListField(models.JSONField):
    def from_db_value(self, value, expression, connection):
        return json.loads(value)

    def get_db_prep_save(self, value, connection):
        value = super().get_db_prep_value(value, connection, prepared=False)

        if value is None:
            return "[]"

        return json.dumps(value)

    def to_python(self, value) -> list:
        if not isinstance(value, list):
            raise ValueError("Not a list")
        return value


class Client(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, null=True)
    surname = models.CharField(max_length=20, null=True)
    patronymic = models.CharField(max_length=20, null=True)
    dob = models.DateTimeField()
    # children = models.JSONField(validators=[ChildModel.model_validate], default=[], encoder=UUIDJsonEncoder)
    children: typing.Sequence[ChildModel] = SchemaField(schema=list[ChildModel], default=[])

    # documentIds = models.JSONField(default=[], null=True)
    # passport = models.JSONField(validators=[PassportModel.model_validate], null=True, encoder=UUIDJsonEncoder)

    documentIds: typing.Sequence[uuid.UUID] = SchemaField(schema=list[uuid.UUID], default=[], null=True)
    passport: PassportModel = SchemaField(schema=PassportModel, null=True)

    # livingAddress = models.JSONField(validators=[AddressModel.model_validate], null=True, encoder=UUIDJsonEncoder)
    # regAddress = models.JSONField(validators=[AddressModel.model_validate], null=True, encoder=UUIDJsonEncoder)
    livingAddress: AddressModel = SchemaField(schema=AddressModel, null=True)
    regAddress: AddressModel = SchemaField(schema=AddressModel, null=True)

    # jobs = models.JSONField(validators=[JobModel.model_validate], encoder=UUIDJsonEncoder)

    jobs: typing.Sequence[JobModel] = SchemaField(schema=list[JobModel], default=[])

    curWorkExp = models.SmallIntegerField(null=True, editable=False)
    typeEducation = models.TextField(choices=EducationType.choices)
    monIncome = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    monExpenses = models.DecimalField(null=True, decimal_places=2, max_digits=10)

    # communications = models.JSONField(validators=[CommunicationModel.model_validate], encoder=UUIDJsonEncoder)
    communications: typing.Sequence[CommunicationModel] = SchemaField(schema=list[CommunicationModel])

    spouse: ClientModel = SchemaField(schema=ClientModel, null=True)

    createdAt = models.DateTimeField(auto_now_add=True, editable=False)
    updatedAt = models.DateTimeField(auto_now=True, editable=False)


