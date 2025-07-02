from fastapi import FastAPI
from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from typing import List
from app.schemas.address import AddressResponse, AddressRequest, AddressUpdatedRequest
from app.services.customer import CustomerService
from app.deps import SessionDep
from uuid import UUID
from app.exceptions import AddressNotFoundException, UserNotFoundException
from app.services.address import AddressService
from app.schemas.customer import Message


app = FastAPI()
router = APIRouter(prefix="/address")
customer_service = CustomerService()
address_service = AddressService()

@router.get("/customer/{customer_id}/", response_model=List[AddressResponse])
def read_customer_adresses(
    customer_id: UUID, 
    session: SessionDep, 
) -> List[AddressResponse]: 
    try: 
        addresses = address_service.get_user_addresses(session, customer_id)
        return addresses
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST)


@router.get("/{address_id}/", response_model=AddressResponse)
def read_address_by_id(
    address_id: UUID, 
    session: SessionDep, 
) -> AddressResponse: 
    try: 
        addresses = address_service.get_address(session, address_id)
        return addresses
    except AddressNotFoundException as e: 
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Address not found")

@router.post("/customer/{id}/", response_model=AddressResponse)
def create_address(
    customer_id: UUID, 
    address_request: AddressRequest,
    session: SessionDep, 
): 
    # try: 
    addresses = address_service.create_address(session, address_request, customer_id)
    return addresses
    # except UserNotFoundException: 
    #     raise HTTPException(HTTPStatus.NOT_FOUND, detail="User not found")
    # except Exception as e:
    #     raise HTTPException(HTTPStatus.BAD_REQUEST)

@router.patch("/{address_id}/", response_model=AddressResponse)
def update_address(
    address_id: UUID,
    session: SessionDep, 
    address_request: AddressUpdatedRequest
): 
    try:
        customer = address_service.update_address(session=session, address=address_request, address_id=address_id)
        return customer
    except AddressNotFoundException as e:
        raise HTTPException(
            status_code=400, 
            detail="Address not found"
        )
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST)


@router.delete("/{address_id}/", response_model=Message)
def delete_address(
    address_id: UUID,
    session: SessionDep, 
): 
    try:
        address_service.delete_address_by_id(session=session, address_id=address_id)
        return Message(message="Address deleted successfully")
    except AddressNotFoundException as e:
        raise HTTPException(
            status_code=400, 
            detail="Address not found"
        )
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST)
