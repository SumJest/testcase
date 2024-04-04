from api.models import Client
from api.pyndantic_models.base_model import UpdatableBaseModel
from api.schemas import NoContent, InClientWithSpouse

from asgiref.sync import sync_to_async


class ClientsService:

    def __init__(self):
        pass

    async def create_client(self, payload: InClientWithSpouse) -> str:
        client = await Client.objects.acreate(**payload.dict())

        return str(client.id)

    async def get_client(self, clientId: str):
        try:
            return await Client.objects.aget(id=clientId)
        except Client.DoesNotExist as exc:
            return exc

    @sync_to_async
    def get_clients(self):
        return Client.objects.all()

    async def delete_client(self, clientId: str) -> None:
        try:
            await Client.objects.filter(pk=clientId).adelete()
            return NoContent()
        except Client.DoesNotExist as exc:
            raise exc

    async def update_client(self, clientId: str, new_client: InClientWithSpouse) -> NoContent:
        try:
            client: Client = await Client.objects.aget(id=clientId)
        except Client.DoesNotExist as exc:
            raise exc

        for key, field_info in new_client.model_fields.items():
            value = getattr(new_client, key)
            original_value = getattr(client, key)

            if isinstance(original_value, UpdatableBaseModel):
                print(f"Rec: Updating {key} - {value}")
                setattr(client, key, getattr(client, key).update(value))
            else:
                print(f"Updating {key} - {value}")
                setattr(client, key, value)
        await client.asave()
        return NoContent()
