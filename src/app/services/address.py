from app.models.address import Address
from .schemas import CustomerCreate
from app.deps import SessionDep
from uuid import UUID

class AddressService():
    def create_address(address: AddressRequest, session: SessionDep) -> User:
        db_user = Address(**address.dict())
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    def create_address(session: Session):
        return session.exec(select(User)).all()


    def create_user(session: Session, user: UserCreate) -> User:
        db_user = User(**user.dict())
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    def update_user(session: Session):
        return session.exec(select(User)).all()

    def get_user_address(session: Session, customer_id: str) -> Address:   
        customer_id = UUID(customer_id)
        statement = select(Address).where(Address.cutomer_id == customer_id)
        return session.exec(statement).first()

    def check_password(session: Session, password: str, customer_id: str): 
        statement = select(Customer.password).where(Customer.id == uscustomer_ider_id)
        result = session.exec(statement).first()
        return result == password


