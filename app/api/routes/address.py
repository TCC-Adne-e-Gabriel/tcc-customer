from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Request, status
from ...deps import SessionDep
from typing import List
from app.schemas.address import AddressResponse, AddressRequest, AddressUpdatedRequest
from app.services.customer import CustomerService
from app.schemas.customer import CustomerRequest, CustomerResponse, PasswordRequest, CustomerUpdateRequest
from app.deps import SessionDep
from uuid import UUID
from app.services.address import AddressService
from app.schemas.customer import Message


app = FastAPI()
router = APIRouter(prefix="/customer")
customer_service = CustomerService()
address_service = AddressService()

@router.get("/{id}/address/", response_model=List[AddressResponse])
def read_customer_adresses(
    id: UUID, 
    session: SessionDep, 
) : 
    addresses = address_service.get_user_addresses(session, id)
    return addresses


@router.get("/address/{address_id}", response_model=AddressResponse)
def read_address_by_id(
    address_id: UUID, 
    session: SessionDep, 
) : 
    addresses = address_service.get_address(session, address_id)
    return addresses


@router.post("/{id}/address/", response_model=AddressResponse)
def read_addresses(
    id: UUID, 
    address_request: AddressRequest,
    session: SessionDep, 
): 
    addresses = address_service.create_address(session, address_request, id)
    return addresses
    

@router.patch("/address/{address_id}", response_model=AddressUpdatedRequest)
def update_customer(
    address_id: UUID,
    session: SessionDep, 
    address_request: AddressUpdatedRequest
): 
    address_by_id = address_service.get_address(session=session, address_id=address_id)
    if(not address_by_id):
        raise HTTPException(
            status_code=400, 
            detail="Address not found"
        )
    customer = address_service.update_address(session=session, address=address_request, current_address=address_by_id)
    return customer

@router.delete("/address/{address_id}", response_model=Message)
def update_customer(
    address_id: UUID,
    session: SessionDep, 
): 
    address = address_service.get_address(session=session, address_id=address_id)
    if(not address):
        raise HTTPException(
            status_code=400, 
            detail="Address not found"
        )
    address_service.delete_address_by_id(session=session, address_id=address_id)
    return Message(message="Address deleted successfully")

