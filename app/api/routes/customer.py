from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from http import HTTPStatus
from ...deps import SessionDep
from app.services.customer import CustomerService
from app.schemas.customer import (
    CustomerRequest,
    CustomerResponse,
    PasswordRequest,
    CustomerUpdateRequest, 
    Token
)
from app.models.customer import Customer
from datetime import timedelta
from typing import Annotated
from app.deps import SessionDep
from uuid import UUID
from app.services.address import AddressService
from app.schemas.customer import Message
from app.core.settings import Settings
from app.services import auth
from typing import List

app = FastAPI()
router = APIRouter(prefix="/customer")
customer_service = CustomerService()
settings = Settings()
address_service = AddressService()


@router.get("/", response_model=List[CustomerResponse], dependencies=[Depends(auth.role_required(["admin"]))])
def read_customers(
    session: SessionDep
) -> CustomerResponse: 
    return customer_service.get_customers(session=session)

@router.get("/{id}/", response_model=CustomerResponse, dependencies=[Depends(auth.role_required(["admin", "service"]))])
def internal_read_customer_by_id(
    session: SessionDep
) -> CustomerResponse: 
    return customer_service.get_customer(session, id)

@router.get("/read/me/", response_model=CustomerResponse)
def read_customer_by_id(
    current_customer: Customer = Depends(auth.role_required(["admin", "user"]))
) -> CustomerResponse: 
    return current_customer


@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(
    session: SessionDep, 
    customer_request: CustomerRequest
) -> CustomerResponse: 

    customer = customer_service.create_customer(session=session, customer=customer_request)
    return customer


@router.patch("/me/", response_model=CustomerResponse)
def update_customer(
    session: SessionDep, 
    customer_request: CustomerUpdateRequest,
    current_customer: Customer = Depends(auth.get_current_customer)
) -> CustomerResponse: 
    
    customer = customer_service.update_customer(session=session, current_customer=current_customer, customer_request=customer_request)
    return customer


@router.delete("/{id}/", dependencies=[Depends(auth.role_required(["admin"]))])
def delete_user(
    session: SessionDep, 
    id: UUID
) -> Message:
        
    address_service.delete_addresses(session, id)
    customer_service.delete_customer(session, id)
    return Message(message="User deleted successfully")

@router.patch("/password/{id}")
def update_password(
    id: UUID, 
    password_request: PasswordRequest, 
    session: SessionDep, 
    current_customer: Customer = Depends(auth.role_required(["admin", "user"]))
) -> Message:

    customer_service.update_password(session, password_request, current_customer) 
    return Message(message="Password updated successfully")

@router.post("/login/", response_model = Token)
async def login_for_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    
    user = auth.authenticate_user(session, form_data)
    access_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)

    access_token = auth.create_access_token(
        data={"sub": str(user.id), "role": user.role}, 
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")
