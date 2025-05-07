from .models import AddressBase
from app.schemas.address import AddressRequest

class AddressCreateRequest(AddressBase):
    pass

class AddressReponse(AddressBase):
    id: str
    created_at: datetime
    updated_at: datetime