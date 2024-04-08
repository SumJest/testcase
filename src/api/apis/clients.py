from typing import List
from uuid import UUID

from ninja import Router

from api.schemas import InClientSchema, OutClientSchema, PatchClientSchema
from api.services.clients import ClientsService
from api.services.pagination import PaginationWithOrdering, apaginate

router = Router()

clients_service = ClientsService()


@router.post('clients/', response={201: str})
async def create_client(request, payload: InClientSchema):

    return await clients_service.create_client(payload)


@router.get('clients/{clientId}/', response={200: OutClientSchema})
async def get_client(request, clientId: UUID):
    return await clients_service.get_client(clientId)


@router.get('clients/', response={200: List[OutClientSchema]})
@apaginate(PaginationWithOrdering)
async def list_clients(request):
    return await clients_service.get_clients()


#
#
@router.delete("clients/{clientId}/", response={204: None})
async def delete_client(request, clientId: UUID):
    await clients_service.delete_client(clientId)
    return 204, None


@router.patch("clients/{clientId}/", response={204: None})
async def update_client(request, clientId: str, payload: PatchClientSchema):
    await clients_service.update_client(clientId, payload)
    return 204, None
