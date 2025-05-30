from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from typing import Optional 
from uuid import UUID, uuid4

class AddressBase(): 
    state: str
    city: str
    complement: Optional[str]
    neighborhood: str
    customer_id: str

class Address():
    id: UUID
    created_at: datetime
    updated_at: datetime