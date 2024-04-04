from typing import List

from ninja import Router

from api.schemas import OutClientWithSpouse, NoContent, InClientWithSpouse
from api.services.clients import ClientsService
from api.services.pagination import PaginationWithOrdering, apaginate

router = Router()

clients_service = ClientsService()


@router.post('clients/', response={201: str})
async def create_client(request, payload: InClientWithSpouse):
    return await clients_service.create_client(payload)


@router.get('clients/{clientId}/', response={200: OutClientWithSpouse})
async def get_client(request, clientId: str):
    return await clients_service.get_client(clientId)


@router.get('clients/', response={200: List[OutClientWithSpouse]})
@apaginate(PaginationWithOrdering)
async def list_clients(request):
    return await clients_service.get_clients()


@router.delete("clients/{clientId}/", response={204: NoContent})
async def delete_client(request, clientId: str):
    return await clients_service.delete_client(clientId)


@router.patch("clients/{clientId}/", response={204: NoContent})
async def update_client(request, clientId: str, payload: InClientWithSpouse):
    return await clients_service.update_client(clientId, payload)
