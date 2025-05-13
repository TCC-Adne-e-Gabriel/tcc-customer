from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Request, status
from ...deps import SessionDep
from app.schemas.customer import CustomerRequest, CustomerResponse, PasswordRequest

app = FastAPI()
router = APIRouter(prefix="/address")


@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerRequest): 
    pass

@router.patch("/password")
def update_password(
    session: SessionDep, 
    password_request: PasswordRequest
):
    pass