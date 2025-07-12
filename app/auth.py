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
from app.context import user_id_context


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
        
def authenticate_user(session: Session, login_request: LoginRequest): 
    customer = customer_service.get_customer_by_email(session, login_request.username)
    if not customer: 
        raise UserNotFoundException
    stored_password_hash = customer.password
    provided_password_hash = login_request.password

    if (not stored_password_hash) or not check_password(stored_password_hash, provided_password_hash): 
        raise InvalidPasswordException
    return customer
    
def get_current_customer_data(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        customer_id = payload.get("sub")
        role = payload.get("role")
        if customer_id is None:
            raise InvalidTokenError
        if role is None: 
            raise InvalidTokenError
        token_data = TokenData(id=customer_id, role=role)
    except InvalidTokenError:
        raise InvalidPasswordException
    user_id_context.set(token_data.id)
    return token_data
    
def role_required(roles: List[str]):
    def checker(decoded_token: TokenData = Depends(get_current_customer_data)):
        if decoded_token.role not in roles:
            raise UnauthorizedException
        return decoded_token
    return checker
