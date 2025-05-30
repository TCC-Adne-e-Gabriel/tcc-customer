from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Depends
from ...deps import SessionDep
from typing import List
from app.schemas.address import AddressResponse, AddressRequest, AddressUpdatedRequest
from app.services.customer import CustomerService
from app.schemas.customer import CustomerRequest, CustomerResponse, PasswordRequest, CustomerUpdateRequest
from app.deps import SessionDep
from uuid import UUID, uuid4
from app.services.address import AddressService
from app.schemas.customer import Message
from core.db import get_db_conn
from typing import Any
from datetime import datetime


app = FastAPI()
router = APIRouter(prefix="/customer")
customer_service = CustomerService()
address_service = AddressService()


router = APIRouter()

@router.get("/{id}")
def get_customer_by_id(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM customer WHERE customer.id = {id}")
    customer = cursor.fetchall()
    cursor.close()
    return {"customer": customer}


@router.get("/address/{id}")
def get_address_by_id(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM address WHERE address.id = {id}")
    address = cursor.fetchall()
    cursor.close()
    return {"address": address}


@router.get("/{id}/address")
def read_customer_adresses(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()
    cursor.execute(f"SELECT a.* FROM address a join customer c on a.customer_id = c.customer_id WHERE c.customer_id = {id};")
    addresses = cursor.fetchall()
    cursor.close()
    return {"addresses": addresses}

@router.post("/")
def create_customer(body, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()
    customer_id = uuid4()
    date_now = datetime.now()
    cursor.execute(
        "INSERT INTO CUSTOMER (id, name, email, password, phone, created_at, updated_at) VALUES"
        f"({customer_id, body.name, body.email, body.password, body.phone, date_now, date_now})")
    conn.commit()
    cursor.close()
    body["id"] = customer_id
    body["updated_at"] = date_now
    body["created_at"] = date_now
    return body


@router.delete("/{id}")
def delete_customer(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()

    cursor.execute("DELETE FROM customer WHERE id = %s", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        raise HTTPException(status_code=404, detail="Customer not found")

    cursor.close()
    return {"message": "Customer deleted successfully"}


@router.delete("/address/{id}")
def delete_address(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM address WHERE id = {id}")
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        raise HTTPException(status_code=404, detail="Address not found")

    cursor.close()
    return {"message": "Address deleted successfully"}


@router.patch("/{id}")
def update_customer(id, customer, conn=Depends(get_db_conn)):
    cursor = conn.cursor()

    fields = []
    values = []

    if customer.name is not None:
        fields.append("name = %s")
        values.append(customer.name)

    if customer.email is not None:
        fields.append("email = %s")
        values.append(customer.email)

    if customer.phone is not None:
        fields.append("phone = %s")
        values.append(customer.phone)

    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    values.append(id)   

    query = f"UPDATE customer SET {', '.join(fields)} WHERE id = {id}"

    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        raise HTTPException(status_code=404, detail="Customer not found")

    cursor.close()
    return {"message": "Customer updated successfully"}


@router.patch("/address/{id}")
def update_address(id, address, conn=Depends(get_db_conn)):
    cursor = conn.cursor()

    fields = []
    values = []

    if address.state is not None:
        fields.append("state = %s")
        values.append(address.state)

    if address.city is not None:
        fields.append("city = %s")
        values.append(address.city)

    if address.complement is not None:
        fields.append("complement = %s")
        values.append(address.complement)

    if address.neighborhood is not None:
        fields.append("neighborhood = %s")
        values.append(address.neighborhood)


    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    values.append(id)   

    query = f"UPDATE address SET {', '.join(fields)} WHERE id = {id}"

    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        raise HTTPException(status_code=404, detail="Address not found")

    cursor.close()
    return {"message": "Address updated successfully"}


@router.patch("/password/{id}")
def update_password(
    id,
    password_request,
    conn=Depends(get_db_conn),     
):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM customer WHERE customer.id = {id}")
    customer = cursor.fetchall()
    cursor.close()
    if(customer.password != password_request.current_password):
        raise HTTPException(
            status_code=400, 
            detail="Incorrect Password"
        )
    
    if(customer.password != password_request.new_password):
        raise HTTPException(
            status_code=400, 
            detail="New password cannot be the same"
        )

    customer = customer_service.get_customer(conn, id)
    customer_service.update_password(conn, password_request.new_password, id) 
    return Message(message="Password updated successfully")