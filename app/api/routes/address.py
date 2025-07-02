from fastapi import APIRouter, HTTPException, Depends, FastAPI
from http import HTTPStatus
from typing import List
from app.schemas.address import AddressResponse, AddressRequest, AddressUpdatedRequest
from app.services.customer import CustomerService
from app.deps import SessionDep
from uuid import UUID
from app.exceptions import AddressNotFoundException, UserNotFoundException
from app.services.address import AddressService
from app.schemas.customer import Message
from app import auth
from app.models.customer import Customer
from app.schemas.customer import TokenData

app = FastAPI()
router = APIRouter(prefix="/address")
customer_service = CustomerService()
address_service = AddressService()

@router.get("/me/", response_model=List[AddressResponse])
def read_customer_adresses(
    session: SessionDep, 
    token_data: TokenData = Depends(auth.role_required(["admin", "user"]))
) -> List[AddressResponse]: 
        
    addresses = address_service.get_user_addresses(session, token_data.id)
    return addresses

@router.get("/{address_id}/", response_model=AddressResponse, dependencies=[Depends(auth.role_required(["admin", "user"]))])
def read_address_by_id(
    address_id: UUID, 
    session: SessionDep, 
) -> AddressResponse: 
        
    addresses = address_service.get_address(session, address_id)
    return addresses

@router.post("/", response_model=AddressResponse)
def create_address(
    address_request: AddressRequest,
    session: SessionDep,     
    token_data: TokenData = Depends(auth.role_required(["admin", "user"]))
): 
    addresses = address_service.create_address(session, address_request, token_data.id)
    return addresses

@router.patch("/{address_id}/", response_model=AddressResponse, dependencies=[Depends(auth.role_required(["admin", "user"]))])
def update_address(
    address_id: UUID,
    session: SessionDep, 
    address_request: AddressUpdatedRequest
): 

    customer = address_service.update_address(session=session, address=address_request, address_id=address_id)
    return customer
    
@router.delete("/{address_id}/", response_model=Message, dependencies=[Depends(auth.role_required(["admin", "user"]))])
def delete_address(
    address_id: UUID,
    session: SessionDep, 
): 
    address_service.delete_address_by_id(session=session, address_id=address_id)
    return Message(message="Address deleted successfully")
