from fastapi import UploadFile, File
from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4

class CustomerBase(): 
    name: str
    email: str
    password: str
    phone: str

class Customer():
    id: UUID
    created_at: datetime
    updated_at: datetime

