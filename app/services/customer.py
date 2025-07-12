from app.models.customer import Customer
from fastapi import Depends
from app.schemas.customer import (
    PasswordRequest,
    CustomerResponse,
    CustomerChangePassword,
    CustomerUpdateRequest,
    CustomerRequest, 
)
from app.schemas.customer import CustomerResponse
from app.core import encrypt
from sqlmodel import Session, select
from app.exceptions import (
    UserNotFoundException, 
    UserEmailAlreadyExistsException,
    InvalidPasswordException, 
    SamePasswordException, 
)
from uuid import UUID
from app.deps import SessionDep
from app.models.customer import Role
from app.customer_logging import logger

class CustomerService():
    def create_customer(self, session: Session, customer: CustomerRequest) -> CustomerResponse:
        customer_email = self.get_customer_by_email(session=session, email=customer.email)
        if(customer_email): 
            raise UserEmailAlreadyExistsException

        customer.password = encrypt.encrypt_data(customer.password)
        customer_data = customer.model_dump()
        customer_data["role"] = Role.user
        db_customer = Customer(**customer_data)
        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)

        logger.audit(f"Customer {db_customer.id} created")
        return db_customer

    def update_customer(self, session: Session, current_customer: Customer, customer_request: CustomerUpdateRequest) -> CustomerResponse:
        if customer_request.email:
            customer = self.get_customer_by_email(session=session, email=customer_request.email)

            if(customer and customer.id != id): 
                raise UserEmailAlreadyExistsException
        
        customer_db = customer_request.model_dump(exclude_none=True)
        current_customer.sqlmodel_update(customer_db)
        session.add(current_customer)
        session.commit()
        session.refresh(current_customer)
        
        logger.info(f"Customer {current_customer.id} updated")
        return current_customer

    def get_customer(self, session: SessionDep, customer_id: UUID) -> CustomerResponse: 
        if not isinstance(customer_id, UUID):
            customer_id = UUID(customer_id)
        statement = select(Customer).where(Customer.id == customer_id)
        customer = session.exec(statement).first()
        if(not customer):
            raise UserNotFoundException
        
        logger.info(f"Customer {customer.id} updated")
        return customer
    
    def get_customers(self, session: Session) -> CustomerResponse: 
        statement = select(Customer).where(Customer)
        customers = session.exec(statement).all()
        return customers

    def update_password(self, session: Session, password_request: PasswordRequest, current_customer: Customer) -> CustomerResponse: 

        if(not encrypt.check_password(password_request.current_password, current_customer.password)): 
            raise InvalidPasswordException
        
        if(encrypt.check_password(current_customer.password, password_request.new_password)):
            raise SamePasswordException
        
        current_customer = self.get_customer(session, id)
        customer_db = CustomerChangePassword(password=password_request.new_password).model_dump()
        current_customer.sqlmodel_update(customer_db)
        session.add(current_customer)
        session.commit()
        session.refresh(current_customer)
        logger.info(f"Password updated")
        return current_customer
    
    def get_customer_by_email(self, session: Session, email: str) -> Customer: 
        statement = select(Customer).where(Customer.email == email)
        result = session.exec(statement).first()
        return result
    
    def delete_customer(self, session: Session, customer_id: UUID): 
        customer = self.get_customer(session=session, customer_id=customer_id)
        session.delete(customer)
        session.commit()
        logger.audit(f"Customer {customer_id} deleted")


