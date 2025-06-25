from fastapi import FastAPI
from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from app.core.encrypt import encrypt_data
from ....deps import SessionDep
from app.services.customer import CustomerService
from app.schemas.customer import (
    CustomerRequest,
    CustomerResponse,
    PasswordRequest,
    CustomerUpdateRequest, 
    LoginRequest
)
from app.deps import SessionDep
from uuid import UUID
from app.services.address import AddressService
from app.schemas.customer import Message
from http import HTTPStatus

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VySGFyZGNvZGVkIiwibmFtZSI6IkFsZ3VucyIsInJvbGUiOiJVc2VyIn0"

app = FastAPI()
router = APIRouter(prefix="/internal/customer")
customer_service = CustomerService()
address_service = AddressService()

@router.get("/{id}", response_model=CustomerResponse)
def read_customer_by_id(
    id: UUID, 
    session: SessionDep, 
) : 
    customer = customer_service.get_customer(session=session, customer_id=id)
    if(not customer): 
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="User with this id not found"
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
            status_code=HTTPStatus.BAD_REQUEST, 
            detail="User with this email already exists"
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
            status_code=HTTPStatus.BAD_REQUEST, 
            detail="User with this email already exists"
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
            status_code=HTTPStatus.BAD_REQUEST, 
            detail="User not found"
        )
    address_service.delete_addresses(session, id)
    customer_service.delete_customer(session, customer)
    return Message(message="User deleted successfully")


@router.patch("/password/{id}")
def update_password(
    id: UUID, 
    session: SessionDep, 
    password_request: PasswordRequest
):
    if(not customer_service.check_password(session, password_request.current_password, id)): 
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, 
            detail="Incorrect Password"
        )
    if(password_request.current_password == password_request.new_password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
            detail="New password cannot be the same"
        )
    customer = customer_service.get_customer(session, id)
    customer_service.update_password(session, password_request.new_password, customer) 
    return Message(message="Password updated successfully")


@router.post("/login/") 
def login(customer_request: LoginRequest, session: SessionDep):
    customer = customer_service.get_customer_by_email(session, customer_request.email)
    stored_password_hash = customer.password
    
    provided_password_hash = encrypt_data(customer_request.password)
    if (not stored_password_hash) or (provided_password_hash != stored_password_hash): 
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Credenciais inválidas")
    
    return {"access_token": TOKEN, "token_type": "bearer"}
        