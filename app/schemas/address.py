from app.models.address import AddressBase
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class AddressCreateRequest(BaseModel):
    state: str
    city: str
    complement: Optional[str]
    neighbothood: str
    customer_id: str


class AddressReponse(AddressBase):
    id: UUID
    created_at: datetime
    updated_at: datetime