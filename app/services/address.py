from ..models.address import Address
from ..schemas.address import AddressRequest
from sqlmodel import Session, select

from uuid import UUID

class AddressService():
    def create_address(address: AddressRequest, session: Session) -> Address:
        db_address = Address(**address.model_dump())
        session.add(db_address)
        session.commit()
        session.refresh(db_address)
        return db_address

    def update_address(session: Session, address: AddressRequest) -> Address:
        db_address = Address(**address.model_dump)
        session.add(db_address)
        session.commit()
        session.refresh(db_address)
        return db_address

    def get_user_address(session: Session, customer_id: str) -> Address:   
        customer_id = UUID(customer_id)
        statement = select(Address).where(Address.cutomer_id == customer_id)
        return session.exec(statement).first()

