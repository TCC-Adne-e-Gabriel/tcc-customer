from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CustomerRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: str

class CustomerUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class CustomerResponse(CustomerRequest):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PasswordRequest(BaseModel):
    current_password: str
    new_password: str 

class Message(BaseModel): 
    message: str

class CustomerChangePassword(BaseModel):
    password: str
