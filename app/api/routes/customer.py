from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Request, status
from ...deps import SessionDep
from typing import Any
from app.services.customer import CustomerService
from app.schemas.customer import CustomerRequest, CustomerResponse, PasswordRequest
from app.deps import SessionDep

app = FastAPI()
router = APIRouter(prefix="/customer")
customer_service = CustomerService()


@router.get("/{id}", response_model=CustomerResponse)
def read_customer_by_id(session: SessionDep, skip: int = 0, limit: int = 100) : 
    customer = customer_service.get_customer(session=session, customer_id=customer.id)
    if(not customer): 
        raise HTTPException(
            status_code=400, 
            detail="User with this email already exists in the system"
        )
    customer = customer_service.create_customer(session=session, customer=customer)
    return customer

@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(*, session: SessionDep, customer: CustomerRequest): 
    customer_email = customer_service.get_customer_by_email(session=session, email=customer.email)
    if(customer_email): 
        raise HTTPException(
            status_code=400, 
            detail="User with this email already exists in the system"
        )
    customer = customer_service.create_customer(session=session, customer=customer)
    return customer


@router.put("/", response_model=CustomerResponse, status_code=201)
def update_user(*, session: SessionDep, customer: CustomerRequest): 
    customer_email = customer_service.get_customer_by_email(session=session, email=customer.email)
    if(customer_email): 
        raise HTTPException(
            status_code=400, 
            detail="User with this email already exists in the system"
        )
    customer = customer_service.create_customer(session=session, customer=customer)
    return customer


@router.patch("/password/{id}")
def update_password(
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

    