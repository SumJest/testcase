from ninja import NinjaAPI
from api.apis.clients import router as client_router


api = NinjaAPI()

api.add_router('', client_router)