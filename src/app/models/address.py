from fastapi import UploadFile, File
from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class AddressBase(SQLModel): 
    state: str
    city: str
    complement: str
    neighbothood: str
    customer_id: str

class Address(AddressBase, table=True):
    id: UUID = Field(default_factory=uuid4,primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)