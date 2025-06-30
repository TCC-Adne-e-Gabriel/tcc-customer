from fastapi import APIRouter

from app.api.routes import customer
from app.api.routes import address 

from app.core.settings import settings

api_router = APIRouter()
api_router.include_router(customer.router)
api_router.include_router(address.router)
