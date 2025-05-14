from app.models.address import AddressBase
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class AddressRequest(BaseModel):
    state: str
    city: str
    complement: Optional[str] = None
    neighbothood: str
    customer_id: Optional[str] = None


class AddressResponse(AddressBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


class AddressUpdatedRequest(BaseModel):
    state: Optional[str] = None
    city: Optional[str] = None
    complement: Optional[str] = None
    neighbothood: Optional[str] = None
