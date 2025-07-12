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
    Token, 
    TokenData
)
from app.models.customer import Customer
from datetime import timedelta
from typing import Annotated
from app.deps import SessionDep
from uuid import UUID
from app.services.address import AddressService
from app.schemas.customer import Message
from app.core.settings import Settings
from app import auth
from typing import List
from app.customer_logging import logger
from app.context import user_context


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
    id: UUID, 
    session: SessionDep
): 
    return customer_service.get_customer(session, id)

@router.get("/read/me/", response_model=CustomerResponse)
def read_customer_by_id(
    session: SessionDep,
    token_data: TokenData = Depends(auth.role_required(["admin", "user"]))
): 
    return customer_service.get_customer(session=session, customer_id=token_data.id)


@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(
    session: SessionDep, 
    customer_request: CustomerRequest
): 
    customer = customer_service.create_customer(session=session, customer=customer_request)
    return customer


@router.patch("/me/", response_model=CustomerResponse)
def update_customer(
    session: SessionDep, 
    customer_request: CustomerUpdateRequest,
    decoded_token: TokenData = Depends(auth.get_current_customer_data)
):  
    user_context.set(decoded_token.id)
    current_customer = customer_service.get_customer(session=session, customer_id=token_data.id)
    customer = customer_service.update_customer(session=session, current_customer=current_customer, customer_request=customer_request)
    return customer


@router.delete("/{id}/")
def delete_user(
    session: SessionDep, 
    id: UUID, 
    decoded_token: TokenData = Depends(auth.role_required(["admin"]))
):
    user_context.set(decoded_token.id)
    address_service.delete_addresses(session, id)
    customer_service.delete_customer(session, id)
    return Message(message="User deleted successfully")

@router.patch("/password/{id}")
def update_password(
    id: UUID, 
    password_request: PasswordRequest, 
    session: SessionDep, 
    decoded_token: TokenData = Depends(auth.role_required(["admin", "user"]))
):
    user_context.set(decoded_token.id)
    current_customer = customer_service.get_customer(session=session, customer_id=token_data.id)
    customer_service.update_password(session, password_request, current_customer) 
    return Message(message="Password updated successfully")

@router.post("/login/", response_model = Token)
async def login_for_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user_context.set(form_data.username)
    user = auth.authenticate_user(session, form_data)
    access_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = auth.create_access_token(
        data={"sub": str(user.id), "name": user.name, "role": user.role}, 
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")
