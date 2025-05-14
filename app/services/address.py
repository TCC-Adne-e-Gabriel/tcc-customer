from app.models.address import Address
from app.schemas.address import AddressResponse, AddressRequest, AddressUpdatedRequest
from sqlmodel import Session, select
from sqlmodel import col, delete, func, select
from typing import List
from uuid import UUID

class AddressService():
    @staticmethod
    def create_address(session: Session, address: AddressRequest, customer_id: UUID) -> AddressResponse:
        address.customer_id = customer_id
        address_data = address.model_dump()
        db_address = Address(**address_data)
        session.add(db_address)
        session.commit()
        session.refresh(db_address)
        return db_address

    @staticmethod
    def update_address(session: Session, address: AddressUpdatedRequest, current_address: Address):
        address_db = address.model_dump()
        current_address.sqlmodel_update(address_db)
        session.add(current_address)
        session.commit()
        session.refresh(current_address)
        return current_address


    @staticmethod
    def delete_addresses(session: Session, customer_id: UUID): 
        statement = delete(Address).where(col(Address.customer_id) == customer_id)
        session.exec(statement)

    @staticmethod
    def delete_address_by_id(session: Session, address_id: UUID): 
        statement = delete(Address).where(col(Address.id) == address_id)
        session.exec(statement)

    @staticmethod
    def get_address(session: Session, address_id: UUID) -> Address: 
        statement = select(Address).where(Address.id == address_id)
        return session.exec(statement).first()

    @staticmethod
    def get_user_addresses(session: Session, customer_id: UUID) -> List[AddressResponse]:   
        statement = select(Address).where(Address.customer_id == customer_id)
        return session.exec(statement).all()

