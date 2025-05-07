from .models import Customer
from .schemas import UserCreate
from sqlmodel import Session

class CustomerService:
    def create_user(session: Session, user: UserCreate) -> User:
        db_user = User(**user.dict())
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    def update_user(session: Session):
        return session.exec(select(User)).all()

    def get_user(customer_id): 
        statement = select(Customer).where(Customer.id == customer_id)
        return session.exec(statement).first()

    def check_password(password: str, customer_id: str): 
        statement = select(Customer.password).where(Customer.id == uscustomer_ider_id)
        result = session.exec(statement).first()
        return result == password


