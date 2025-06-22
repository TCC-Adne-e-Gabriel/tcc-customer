from app.models.customer import Customer
from app.schemas.customer import CustomerRequest, CustomerResponse, CustomerChangePassword
from sqlmodel import Session, select
from app.core.encrypt import encrypt_data
from uuid import UUID

class CustomerService():
    def create_customer(self, session: Session, customer: CustomerRequest) -> CustomerResponse:
        customer.password = encrypt_data(customer.password)
        customer_data = customer.model_dump()
        db_customer = Customer(**customer_data)
        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)
        return db_customer

    def update_customer(self, session: Session, customer: CustomerRequest, current_customer: Customer):
        customer_db = customer.model_dump(exclude_none=True)
        print(customer_db)
        current_customer.sqlmodel_update(customer_db)
        session.add(current_customer)
        session.commit()
        session.refresh(current_customer)
        return current_customer

    def get_customer(self, session: Session, customer_id: UUID) -> Customer: 
        statement = select(Customer).where(Customer.id == customer_id)
        return session.exec(statement).first()

    def check_password(self, session: Session, password: str, customer_id: UUID): 
        statement = select(Customer.password).where(Customer.id == customer_id)
        result = session.exec(statement).first()
        return result == password
    
    def update_password(self, session: Session, password: str, current_customer: Customer): 
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
    
    def delete_customer(self, session: Session, current_customer: Customer): 
        session.delete(current_customer)
        session.commit()
    


