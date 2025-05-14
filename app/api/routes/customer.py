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


@router.get("/{id}", response_model=CustomerResponse)
def read_customer_by_id(
    id: UUID, 
    session: SessionDep, 
    skip: int = 0, 
    limit: int = 100
) : 
    customer = customer_service.get_customer(session=session, customer_id=id)
    if(not customer): 
        raise HTTPException(
            status_code=400, 
            detail="User with this id doesnt exist"
        )
    return customer

@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(
    session: SessionDep, 
    customer: CustomerRequest
): 
    customer_email = customer_service.get_customer_by_email(session=session, email=customer.email)
    if(customer_email): 
        raise HTTPException(
            status_code=400, 
            detail="User with this email already exists in the system"
        )
    customer = customer_service.create_customer(session=session, customer=customer)
    return customer


@router.patch("/{id}", response_model=CustomerResponse)
def update_customer(
    id: UUID,
    session: SessionDep, 
    customer_request: CustomerUpdateRequest
): 
    customer_email = customer_service.get_customer_by_email(session=session, email=customer_request.email)
    if(customer_email and customer_email.id != id): 
        raise HTTPException(
            status_code=400, 
            detail="User with this email already exists in the system"
        )
    customer_id = customer_service.get_customer(session=session, customer_id=id)
    customer = customer_service.update_customer(session=session, customer=customer_request, current_customer=customer_id)
    return customer


@router.delete("/{id}")
def delete_user(
    id: UUID, 
    session: SessionDep, 
):
    customer = customer_service.get_customer(session, id)
    if(not customer_service.get_customer(session, id)): 
        raise HTTPException(
            status_code=400, 
            detail="User not found"
        )
    address_service.delete_addresses(session, id)
    customer_service.delete_customer(session, customer)
    return Message(message="User deleteds uccessfully")


@router.patch("/password/{id}")
def update_password(
    id: UUID, 
    session: SessionDep, 
    password_request: PasswordRequest
):
    if(not customer_service.check_password(session, password_request.current_password, id)): 
        raise HTTPException(
            status_code=400, 
            detail="Incorrect Password"
        )
    if(password_request.current_password == password_request.new_password):
        raise HTTPException(
            status_code=400, 
            detail="New password cannot be the same"
        )
    customer = customer_service.get_customer(session, id)
    customer_service.update_password(session, password_request.new_password, customer) 
    return Message(message="Password updated successfully")


@router.get("/{id}/address/", response_model=List[AddressResponse])
def read_customer_by_id(
    id: UUID, 
    session: SessionDep, 
) : 
    addresses = address_service.get_user_addresses(session, id)
    return addresses


@router.get("/address/{address_id}", response_model=AddressResponse)
def read_customer_by_id(
    address_id: UUID, 
    session: SessionDep, 
) : 
    addresses = address_service.get_address(session, address_id)
    return addresses


@router.post("/{id}/address/", response_model=AddressResponse)
def read_customer_by_id(
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

