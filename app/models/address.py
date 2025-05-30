from datetime import datetime, timezone
from sqlmodel import Field, SQLModel
from typing import Optional 
from uuid import UUID, uuid4

class AddressBase(SQLModel): 
    state: str
    city: str
    complement: Optional[str]
    neighbothood: str
    customer_id: str

class Address(AddressBase, table=True):
    id: UUID = Field(default_factory=uuid4,primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)