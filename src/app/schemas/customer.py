from .models import CustomerBase
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class CustomerRequest(CustomerBase):
    pass

class CustomerResponse(AddressBase):
    id: str
    created_at: datetime
    updated_at: datetime

class PasswordRequest(SQLModel):
    current_password: str
    new_password: str 