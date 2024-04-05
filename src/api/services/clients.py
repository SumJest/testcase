import datetime
from typing import List, Callable
from uuid import UUID

from django.db.models import QuerySet, Model, Prefetch, prefetch_related_objects
from django.http import Http404
from pydantic import BaseModel

from api.models import Client, Address, Passport, Job, Child, Communication
from api.schemas import InClientSchema, InAddress, InPassport, InJob, InChild, InCommunication, PatchClientSchema, \
    PatchWithoutClientSchema, PatchJob, PatchChild

from asgiref.sync import sync_to_async


class ClientsService:

    def __init__(self):
        pass

    def create_address(self, address: dict):
        return Address.objects.create(**address)

    def create_passport(self, passport: dict):
        return Passport.objects.create(**passport)

    def create_job(self, job: dict, client: Client):
        if job["factAddress"]:
            factAddress = self.create_address(job["factAddress"])
        else:
            factAddress = None
        if job["jurAddress"]:
            jurAddress = self.create_address(job["jurAddress"])
        else:
            jurAddress = None

        job.update({'factAddress': factAddress, 'jurAddress': jurAddress, 'client': client})
        Job.objects.create(**job)

    def create_child(self, child: dict, client: Client):
        Child.objects.create(**child, client=client)

    def create_communication(self, communication: dict, client: Client):
        Communication.objects.create(**communication, client=client)

    def __create_client(self, payload: InClientSchema) -> Client:
        if payload.livingAddress:
            livingAddress = self.create_address(payload.livingAddress.dict())
        else:
            livingAddress = None
        if payload.regAddress:
            regAddress = self.create_address(payload.regAddress.dict())
        else:
            regAddress = None
        if payload.passport:
            passport = self.create_passport(payload.passport.dict())
        else:
            passport = None

        if payload.spouse:
            spouse = self.__create_client(payload.spouse)
        else:
            spouse = None

        payload_dict = payload.dict()
        payload_dict.update({'livingAddress': livingAddress, 'regAddress': regAddress, 'passport': passport,
                             'spouse': spouse})

        children = payload_dict.pop("children")
        communications = payload_dict.pop("communications")
        jobs = payload_dict.pop("jobs")
        print(payload_dict)
        client = Client.objects.create(**payload_dict)

        for communication in communications:
            self.create_communication(communication, client)

        for child in children:
            self.create_child(child, client)

        for job in jobs:
            self.create_job(job, client)

        return client

    @sync_to_async
    def create_client(self, payload: InClientSchema):
        return str((self.__create_client(payload)).id)

    def resolve_clients_query_set(self) -> QuerySet:
        return (Client.objects.select_related('passport', 'livingAddress', 'regAddress', 'spouse',
                                              'spouse__livingAddress', 'spouse__passport', 'spouse__regAddress')
                .prefetch_related('communication_set', 'job_set', 'spouse__communication_set', 'child_set',
                                  'spouse__child_set', 'spouse__job_set',)
                .prefetch_related('job_set__jurAddress', 'job_set__factAddress',
                                  'spouse__job_set__factAddress', 'spouse__job_set__jurAddress'))

    @sync_to_async
    def get_client(self, clientId: UUID):
        client = self.resolve_clients_query_set().filter(id=clientId).first()
        if not client:
            raise Http404()
        return client

    @sync_to_async
    def get_clients(self):
        return self.resolve_clients_query_set().all()

    async def delete_client(self, clientId: UUID) -> None:
        try:
            await Client.objects.filter(pk=clientId).adelete()
        except Client.DoesNotExist as exc:
            raise Http404(str(exc))

    def update_submodel(self, sub_model: Model, dump: dict) -> bool:
        if sub_model and dump is None:
            sub_model.delete()
        updated = False
        for key, value in dump.items():
            if type(value) is dict:

                if getattr(sub_model, key, None) is None:
                    setattr(sub_model, key, self.create_address(value))
                    updated = True
                    continue

                updated = self.update_submodel(getattr(sub_model, key), value)
                continue

            if getattr(sub_model, key, None) != value:
                setattr(sub_model, key, value)

                updated = True
        if updated:
            sub_model.save()
        return updated

    def update_model_list(self, client: Client, list_of_models: List | None, model_class: Model,
                          creation_func: Callable):
        if list_of_models is None:
            return
        existing_ids = set(model_class.objects.values_list('id', flat=True).filter(client=client).all())
        available_ids = {obj.id for obj in list_of_models}

        model_class.objects.filter(pk__in=existing_ids - available_ids).delete()
        updated = False
        for model in list_of_models:
            model_dump = model.model_dump(exclude_unset=True, exclude_none=True)
            if model.id is None:
                creation_func(model_dump, client)
                updated = True
                continue
            try:
                updating_model = model_class.objects.get(pk=model.id)
            except:
                continue
            updated = updated or self.update_submodel(updating_model, model_dump)
        if updated:
            client.save()

    def update_children(self, client: Client, children: List[PatchChild] | None):
        if children is None:
            return
        updated = False
        for child in children:
            model_dump = child.model_dump(exclude_unset=True, exclude_none=True)
            if child.id is None:
                self.create_child(model_dump, client)
                updated = True
                continue
            updated = updated or self.update_submodel(Job.objects.get(child.id), model_dump)
        if updated:
            client.save()

    def __update_client(self, clientId: UUID, new_client: PatchWithoutClientSchema) -> None:
        try:
            client = Client.objects.get(pk=clientId)
        except Client.DoesNotExist as exc:
            raise Http404(str(exc))
        if new_client is None:
            client.delete()
            return
        client_simple_fields = {'name', 'surname', 'patronymic', 'dob', 'documentId', 'curWorkExp',
                                'typeEducation', 'monIncome', 'monExpenses'}
        update_dump_client = new_client.model_dump(exclude_unset=True, include=client_simple_fields)
        updated = False
        for key, value in update_dump_client.items():
            if getattr(client, key, None) != updated:
                setattr(client, key, value)
                updated = True

        # passport
        passport_simple_fields = {'series', 'number', 'giver', 'dateIssued'}
        if new_client.passport:
            update_dump = new_client.passport.model_dump(exclude_unset=True, include=passport_simple_fields)
        else:
            update_dump = None
        updated = updated or self.update_submodel(client.passport, update_dump)

        # addresses
        if new_client.livingAddress:
            update_dump = new_client.livingAddress.model_dump(exclude_unset=True)
        else:
            update_dump = None
        updated = updated or self.update_submodel(client.livingAddress, update_dump)

        if new_client.regAddress:
            update_dump = new_client.regAddress.model_dump(exclude_unset=True)
        else:
            update_dump = None
        updated = updated or self.update_submodel(client.regAddress, update_dump)
        if updated:
            client.save()
        # spouse
        if hasattr(new_client, 'spouse'):
            if client.spouse:
                self.__update_client(client.spouse.id, new_client.spouse)
            else:
                if new_client.spouse is not None:
                    spouse = self.__create_client(new_client.spouse)
                    client.spouse = spouse
                    client.save()

        # jobs
        self.update_model_list(client, new_client.jobs, Job, self.create_job)
        # children
        self.update_model_list(client, new_client.children, Child, self.create_child)
        # communications
        self.update_model_list(client, new_client.communications, Communication, self.create_communication)

    @sync_to_async
    def update_client(self, clientId: UUID, new_client: PatchWithoutClientSchema) -> None:
        self.__update_client(clientId, new_client)
