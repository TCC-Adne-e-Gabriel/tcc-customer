from datetime import datetime, timezone
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional 
from uuid import UUID, uuid4
from app.models.customer import Customer

class Address(SQLModel, table=True):
    state: str
    city: str
    complement: Optional[str]
    neighborhood: str
    id: UUID = Field(default_factory=uuid4,primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    customer_id: UUID = Field(default=None, foreign_key="customer.id")

    customer: Optional[Customer] = Relationship(back_populates="addresses")

