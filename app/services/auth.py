from app.models.customer import Customer
from fastapi import Depends
from app.schemas.customer import (
    LoginRequest, 
    TokenData, 
)
from app.services.customer import CustomerService
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.encrypt import encrypt_data
from sqlmodel import Session, select
from app.core.encrypt import encrypt_data
from app.exceptions import (
    InvalidPasswordException, 
    InvalidTokenException
)
from typing import Annotated
import jwt
from jwt import InvalidTokenError
from datetime import datetime, timezone, timedelta
from app.core.settings import Settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
settings = Settings()

class AuthService():
    def __init__(self): 
        self.customer_service = CustomerService()

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
        

    async def get_current_user(self, session: Session, token: Annotated[str, Depends(oauth2_scheme)]):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise InvalidTokenException
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise InvalidTokenException
        user = self.get_user_by_email(session=session, email=token_data.username)
        if user is None:
            raise InvalidTokenException
        return user

    async def get_current_active_user(
        self, 
        session: Session
    ):
        current_user = self.get_current_user(session=session)
        return current_user
    
    def authenticate_user(self, session: Session, login_request: LoginRequest): 
        customer = self.customer_service.get_customer_by_email(session, login_request.username)
        stored_password_hash = customer.password
        
        provided_password_hash = encrypt_data(login_request.password)
        if (not stored_password_hash) or (provided_password_hash != stored_password_hash): 
            raise InvalidPasswordException
        return customer
            