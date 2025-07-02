from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4
from typing import List
from enum import Enum

class Role(str, Enum): 
    user = "user"
    admin = "admin"
    service = "service"

class Customer(SQLModel, table=True):
    name: str
    email: str
    password: str
    phone: str
    id: UUID = Field(default_factory=uuid4,primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    role: Role
    active: bool

    addresses: List["Address"] = Relationship(back_populates="customer")
