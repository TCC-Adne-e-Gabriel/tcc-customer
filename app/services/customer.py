from app.models.customer import Customer
from app.schemas.customer import CustomerRequest, CustomerResponse
from sqlmodel import Session, select

class CustomerService:
    @staticmethod
    def create_customer(session: Session, customer: CustomerRequest) -> CustomerResponse:
        customer_data = customer.model_dump()
        db_customer = Customer(**customer_data)
        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)
        return db_customer

    def update_customer(session: Session, customer: CustomerRequest):
        return session.exec(select(Customer)).all()
        session.add(customer)

    def get_customer(session: Session, customer_id): 
        statement = select(Customer).where(Customer.id == customer_id)
        return session.exec(statement).first()

    def check_password(session: Session, password: str, customer_id: str): 
        statement = select(Customer.password).where(Customer.id == customer_id)
        result = session.exec(statement).first()
        return result == password
    
    def get_customer_by_email(session: Session, email: str) -> Customer: 
        statement = select(Customer).where(Customer.email == email)
        result = session.exec(statement).first()
        print("oii", result)
        return result
    


