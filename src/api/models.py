import json
import typing
import uuid

from django.db import models
from django_softdelete.models import SoftDeleteModel
from django_pydantic_field import SchemaField


# Create your models here.
class CommunicationType(models.TextChoices):
    email = "email", "Электронная почта"
    phone = "phone", "Мобильный телефон"


class JobType(models.TextChoices):
    main = "main", "Основная работа"
    part_time = "part-time", "Частичная занятость"


class EducationType(models.TextChoices):
    secondary = "secondary", "Среднее"
    secondarySpecial = "secondarySpecial", "Среднее специальное"
    incompleteHigher = "incompleteHigher", "Незаконченное высшее"
    higher = "higher", "Высшее"
    twoOrMoreHigher = "twoOrMoreHigher", "Два и более высших образований"
    academicDegree = "academicDegree", "Академическая степень"


class Passport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    series = models.CharField(max_length=4, null=False)
    number = models.CharField(max_length=6, null=False)
    giver = models.CharField(max_length=100, null=False)
    dateIssued = models.DateTimeField(null=False)
    createdAt = models.DateTimeField(auto_now_add=True, editable=False)
    updatedAt = models.DateTimeField(auto_now=True, editable=False)


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    zipCode = models.CharField(max_length=6, null=True)
    country = models.CharField(max_length=20, null=True)
    region = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=20, null=True)
    apartment = models.CharField(max_length=20, null=True)
    createdAt = models.DateTimeField(auto_now_add=True, editable=False)
    updatedAt = models.DateTimeField(auto_now=True, editable=False)


class Client(SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, null=True)
    surname = models.CharField(max_length=20, null=True)
    patronymic = models.CharField(max_length=20, null=True)
    dob = models.DateTimeField(null=True)

    documentIds: typing.Sequence[uuid.UUID] = SchemaField(schema=list[uuid.UUID], default=[], null=True)
    passport = models.OneToOneField(to=Passport, on_delete=models.SET_NULL, null=True, unique=True)
    livingAddress = models.OneToOneField(to=Address, on_delete=models.SET_NULL, null=True,
                                         related_name="client_living_address")
    regAddress = models.OneToOneField(to=Address, on_delete=models.SET_NULL, null=True,
                                      related_name="client_reg_address")

    curWorkExp = models.SmallIntegerField(null=True, editable=True)
    typeEducation = models.CharField(choices=EducationType.choices, max_length=20)
    monIncome = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    monExpenses = models.DecimalField(null=True, decimal_places=2, max_digits=10)

    spouse = models.ForeignKey(to="self", null=True, on_delete=models.SET_NULL)

    createdAt = models.DateTimeField(auto_now_add=True, editable=False)
    updatedAt = models.DateTimeField(auto_now=True, editable=False)


class Child(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, null=True)
    surname = models.CharField(max_length=20, null=True)
    patronymic = models.CharField(max_length=20, null=True)
    dob = models.DateTimeField(null=True)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)


class Job(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(choices=JobType.choices, null=True, max_length=10)
    dateEmp = models.DateTimeField(null=True)
    dateDismissal = models.DateTimeField(null=True)
    monIncome = models.DecimalField(null=True, decimal_places=2, max_digits=10)
    tin = models.CharField(max_length=15, null=True)
    factAddress = models.OneToOneField(to=Address, null=True, on_delete=models.SET_NULL, related_name="job_fact_address")
    jurAddress = models.OneToOneField(to=Address, null=True, on_delete=models.SET_NULL, related_name="job_jur_address")
    phoneNumber = models.CharField(max_length=15)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)

    createdAt = models.DateTimeField(auto_now_add=True, editable=False)
    updatedAt = models.DateTimeField(auto_now=True, editable=False)


class Communication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(choices=CommunicationType.choices, null=False, max_length=10)
    value = models.CharField(max_length=256, null=False)

    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
