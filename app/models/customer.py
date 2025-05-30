from fastapi import UploadFile, File
from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4

class CustomerBase(SQLModel): 
    name: str
    email: str
    password: str
    phone: str

class Customer(CustomerBase, table=True):
    id: UUID = Field(default_factory=uuid4,primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

