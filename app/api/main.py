from fastapi import APIRouter

from app.api.routes.public import customer
from app.api.routes.internal import internal_customer

from app.core.settings import settings

api_router = APIRouter()
api_router.include_router(customer.router)
api_router.include_router(internal_customer.router)


