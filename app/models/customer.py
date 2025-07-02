from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4
from typing import List

class Customer(SQLModel, table=True):
    name: str
    email: str
    password: str
    phone: str
    id: UUID = Field(default_factory=uuid4,primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

    addresses: List["Address"] = Relationship(back_populates="customer")
