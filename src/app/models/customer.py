from fastapi import UploadFile, File
from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4

class CustomerBase(SQLModel): 
    name: str
    email: str
    password: str
    name: str
    phone: str

class Customer(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4,primary_key=True)
    name: str
    email: str
    password: str
    name: str
    phone: str
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
