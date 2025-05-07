from fastapi import APIRouter

from app.routes import product

api_router = APIRouter()
api_router.include_router(product.router)
