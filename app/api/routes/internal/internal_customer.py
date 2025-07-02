from fastapi import FastAPI
from fastapi import APIRouter, HTTPException
from http import HTTPStatus
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
from app.exceptions import UserNotFoundException, SamePasswordException, InvalidPasswordException, UserEmailAlreadyExistsException
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
    try:
        customer = customer_service.get_customer(session=session, customer_id=id)
        return customer
    except UserNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="User not found"
        )
    except Exception: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )

@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(
    session: SessionDep, 
    customer_request: CustomerRequest
): 
    try: 
        customer = customer_service.create_customer(session=session, customer=customer_request)
        return customer
    except UserEmailAlreadyExistsException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
            detail="User with this email already exists"
        )
    except Exception: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )


@router.patch("/{id}", response_model=CustomerResponse)
def update_customer(
    id: UUID,
    session: SessionDep, 
    customer_request: CustomerUpdateRequest
): 
    try: 
        customer = customer_service.update_customer(session=session, customer_id=id, customer_request=customer_request)
        return customer
    except UserEmailAlreadyExistsException:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
            detail="User with this email already exists"
        )
    except UserNotFoundException:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="User not found"
        )
    except Exception: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )


@router.delete("/{id}")
def delete_user(
    id: UUID, 
    session: SessionDep, 
):
    try:
        address_service.delete_addresses(session, id)
        customer_service.delete_customer(session, id)
        return Message(message="User deleted successfully")
    except UserNotFoundException: 
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail="User not found"
        )
    except Exception: 
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, 
        )

        