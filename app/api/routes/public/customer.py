from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from http import HTTPStatus
from ....deps import SessionDep
from app.services.customer import CustomerService
from app.schemas.customer import (
    CustomerRequest,
    CustomerResponse,
    PasswordRequest,
    CustomerUpdateRequest, 
    LoginRequest, 
    Token
)
from datetime import timedelta
from typing import Annotated
from app.deps import SessionDep
from uuid import UUID
from app.exceptions import UserNotFoundException, SamePasswordException, InvalidPasswordException, UserEmailAlreadyExistsException
from app.services.address import AddressService
from app.services.auth import AuthService
from app.schemas.customer import Message
from http import HTTPStatus
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.settings import Settings

app = FastAPI()
router = APIRouter(prefix="/customer")
customer_service = CustomerService()
settings = Settings()
auth_service = AuthService()
address_service = AddressService()

@router.get("/{id}/", response_model=CustomerResponse)
def read_customer_by_id(
    id: UUID, 
    session: SessionDep, 
) -> CustomerResponse: 
    try:
        customer = customer_service.get_customer(session=session, customer_id=id)
        return customer
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="User not found"
        )
    except Exception as e: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )

@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(
    session: SessionDep, 
    customer_request: CustomerRequest
) -> CustomerResponse: 
    try: 
        customer = customer_service.create_customer(session=session, customer=customer_request)
        return customer
    except UserEmailAlreadyExistsException as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
            detail="User with this email already exists"
        )
    except Exception as e: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )


@router.patch("/{id}", response_model=CustomerResponse)
def update_customer(
    id: UUID,
    session: SessionDep, 
    customer_request: CustomerUpdateRequest
) -> CustomerResponse: 
    try: 
        customer = customer_service.update_customer(session=session, customer_id=id, customer_request=customer_request)
        return customer
    except UserEmailAlreadyExistsException as e:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
            detail="User with this email already exists"
        )
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="User not found"
        )
    except Exception as e: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )


@router.delete("/{id}/")
def delete_user(
    id: UUID, 
    session: SessionDep, 
) -> Message:
    try:
        address_service.delete_addresses(session, id)
        customer_service.delete_customer(session, id)
        return Message(message="User deleted successfully")
    except UserNotFoundException as e: 
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="User not found"
        )
    except Exception as e: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )


@router.patch("/password/{id}")
def update_password(
    id: UUID, 
    session: SessionDep, 
    password_request: PasswordRequest
) -> Message:
    try: 
        customer_service.update_password(session, password_request, id) 
        return Message(message="Password updated successfully")
    except SamePasswordException as e: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
            detail="New password cannot be the same"
        )
    except InvalidPasswordException:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, 
            detail="Incorrect Password"
        )
    except Exception as e: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )
        

@router.post("/login/")
async def login_for_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    try:
        user = auth_service.authenticate_user(session, form_data)
        access_token_expires = timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
        access_token = auth_service.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
    except InvalidPasswordException: 
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    except Exception as e: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )
