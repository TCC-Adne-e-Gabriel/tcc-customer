from app.models.address import Address
from app.schemas.address import AddressResponse, AddressRequest, AddressUpdatedRequest
from sqlmodel import Session, select, delete
from typing import List
from uuid import UUID
from http import HTTPStatus
from app.services.customer import CustomerService
from app.exceptions import AddressNotFoundException

class AddressService():
    def __init__(self): 
        self.customer_service = CustomerService()

    def create_address(self, session: Session, address: AddressRequest, customer_id: UUID) -> AddressResponse:
        self.customer_service.get_customer(session=session, customer_id=customer_id)
        address_data = address.model_dump()
        address_data["customer_id"] = customer_id
        db_address = Address(**address_data)
        session.add(db_address)
        session.commit()
        session.refresh(db_address)
        return db_address

    def update_address(self, session: Session, address: AddressUpdatedRequest, address_id: UUID) -> AddressResponse:
        current_address = self.get_address(session=session, address_id=address_id)
        if(not current_address):
            raise AddressNotFoundException
        address_db = address.model_dump(exclude_none=True)
        current_address.sqlmodel_update(address_db)
        session.add(current_address)
        session.commit()
        session.refresh(current_address)
        return current_address

    def delete_addresses(self, session: Session, customer_id: UUID): 
        statement = delete(Address).where(Address.customer_id == customer_id)
        session.exec(statement)

    def delete_address_by_id(self, session: Session, address_id: UUID): 
        current_address = self.get_address(session=session, address_id=address_id)
        if(not current_address):
            raise AddressNotFoundException
        session.delete(current_address)
        session.commit()

    def get_address(self, session: Session, address_id: UUID) -> AddressResponse: 
        statement = select(Address).where(Address.id == address_id)
        address = session.exec(statement).first()
        if(not address):
            raise AddressNotFoundException

        return address

    def get_user_addresses(self, session: Session, customer_id: UUID) -> List[AddressResponse]:    
        statement = select(Address).where(Address.customer_id == customer_id)
        return session.exec(statement).all()
