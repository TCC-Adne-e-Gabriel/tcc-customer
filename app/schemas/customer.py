from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class CustomerRequest(BaseModel):
    name: str
    email: str
    password: str
    phone: str

class CustomerResponse(CustomerRequest):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PasswordRequest(BaseModel):
    current_password: str
    new_password: str 