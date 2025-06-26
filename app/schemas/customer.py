from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CustomerBase(BaseModel): 
    name: str
    email: str
    phone: str

class CustomerResponse(CustomerBase): 
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CustomerRequest(CustomerBase):
    password: str

class CustomerUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class PasswordRequest(BaseModel):
    current_password: str
    new_password: str 

class Message(BaseModel): 
    message: str

class CustomerChangePassword(BaseModel):
    password: str

class LoginRequest(BaseModel): 
    email: str
    password: str