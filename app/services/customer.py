from app.models.customer import Customer
from app.schemas.customer import (
    PasswordRequest,
    CustomerResponse,
    CustomerChangePassword,
    CustomerUpdateRequest,
    CustomerRequest, 
    LoginRequest
)
from app.schemas.customer import CustomerResponse
from app.core.encrypt import encrypt_data
from sqlmodel import Session, select
from app.core.encrypt import encrypt_data
from app.exceptions import (
    UserNotFoundException, 
    UserEmailAlreadyExistsException,
    InvalidPasswordException, 
    SamePasswordException
)
from uuid import UUID

class CustomerService():
    def create_customer(self, session: Session, customer: CustomerRequest) -> CustomerResponse:
        customer_email = self.get_customer_by_email(session=session, email=customer.email)
        if(customer_email): 
            raise UserEmailAlreadyExistsException

        customer.password = encrypt_data(customer.password)
        customer_data = customer.model_dump()
        db_customer = Customer(**customer_data)
        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)
        return db_customer

    def update_customer(self, session: Session, customer_id: UUID, customer_request: CustomerUpdateRequest) -> CustomerResponse:
        
        if customer_request.email:
            customer = self.customer_service.get_customer_by_email(session=session, email=customer_request.email)

            if(customer and customer.id != id): 
                raise UserEmailAlreadyExistsException
            
        customer = self.get_customer(session=session, customer_id=customer_id)
        if not customer:
            raise UserNotFoundException
        
        customer_db = customer.model_dump(exclude_none=True)
        customer.sqlmodel_update(customer_db)
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer

    def get_customer(self, session: Session, customer_id: UUID) -> CustomerResponse: 
        statement = select(Customer).where(Customer.id == customer_id)
        customer = session.exec(statement).first()
        if(not customer):
            raise UserNotFoundException
        return customer

    def check_password(self, session: Session, password: str, customer_id: UUID): 
        statement = select(Customer.password).where(Customer.id == customer_id)
        result = session.exec(statement).first()
        return result == password
    
    def update_password(self, session: Session, password: str, password_request: PasswordRequest) -> CustomerResponse: 
        if(not self.check_password(session, password_request.current_password, id)): 
            raise InvalidPasswordException
        if(password_request.current_password == password_request.new_password):
            raise SamePasswordException
        current_customer = self.get_customer(session, id)
        customer_db = CustomerChangePassword(password=password).model_dump()
        current_customer.sqlmodel_update(customer_db)
        session.add(current_customer)
        session.commit()
        session.refresh(current_customer)
        return current_customer
    
    def get_customer_by_email(self, session: Session, email: str) -> Customer: 
        statement = select(Customer).where(Customer.email == email)
        result = session.exec(statement).first()
        return result
    
    def login(self, session: Session, login_request: LoginRequest): 
        customer = self.get_customer_by_email(session, login_request.email)
        stored_password_hash = customer.password
        
        provided_password_hash = encrypt_data(login_request.password)
        if (not stored_password_hash) or (provided_password_hash != stored_password_hash): 
            raise InvalidPasswordException
        
    def delete_customer(self, session: Session, customer_id: UUID): 
        customer = self.get_customer(session=session, customer_id=customer_id)
        if not customer:
            raise UserNotFoundException
        session.delete(customer)
        session.commit()
