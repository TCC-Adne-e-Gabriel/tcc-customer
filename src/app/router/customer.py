from typing import Union
from app.customer.schemas import CustomerResponse
from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Request, status
from app.deps import SessionDep
from app.schemas.customer import PasswordRequest

app = FastAPI()
router = APIRouter(prefix="/customer")


@router.post("/", response_model=CustomerResponse)
def create_customer(customer: CustomerRequest): 


@router.patch("/password")
def update_password(
    session: SessionDep, 
    password_request: PaswordRequest
):
