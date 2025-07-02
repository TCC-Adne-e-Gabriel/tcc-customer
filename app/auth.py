from app.models.customer import Customer
from fastapi import Depends
from app.schemas.customer import (
    LoginRequest, 
    TokenData, 
)
from app.services.customer import CustomerService
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.encrypt import encrypt_data, check_password
from sqlmodel import Session, select
from app.exceptions import (
    InvalidPasswordException, 
    InvalidTokenException, 
    UserNotFoundException, 
    UnauthorizedException,
)
from app.deps import SessionDep
from http import HTTPStatus
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timezone, timedelta
from app.core.settings import Settings
from typing import List


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = Settings()
customer_service = CustomerService()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
        
async def get_current_customer(session: SessionDep, token: str = Depends(oauth2_scheme)) -> Customer:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise InvalidTokenException
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise InvalidTokenException
    user = customer_service.get_customer(session=session, customer_id=token_data.username)
    if not user:
        raise UserNotFoundException
    return user

async def get_current_active_customer(
    self, 
    session: Session, 
    token: str
):
    current_customer = self.get_current_customer(session=session, token=token)
    return current_customer
    
def authenticate_user(session: Session, login_request: LoginRequest): 
    customer = customer_service.get_customer_by_email(session, login_request.username)
    if not customer: 
        raise UserNotFoundException
    stored_password_hash = customer.password
    provided_password_hash = login_request.password

    if (not stored_password_hash) or not check_password(stored_password_hash, provided_password_hash): 
        raise InvalidPasswordException
    return customer
    
def role_required(roles: List[str]):
    async def checker(current_customer: Customer = Depends(get_current_customer)):
        if not current_customer.role.value in roles:
            raise UnauthorizedException
        return current_customer
    return checker
