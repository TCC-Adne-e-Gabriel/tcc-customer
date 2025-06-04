from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import List
from app.services.customer import CustomerService
from uuid import UUID, uuid4
from app.core.encrypt import encrypt_data
from app.core.db import get_db_conn
from typing import Any
from datetime import datetime

app = FastAPI()
router = APIRouter(prefix="/customer")
customer_service = CustomerService()
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VySGFyZGNvZGVkIiwibmFtZSI6IkFsZ3VucyIsInJvbGUiOiJVc2VyIn0"


@router.get("/{id}/")
def get_customer_by_id(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer.id = %s", (id,))
    customer = cursor.fetchone()    
    cursor.close()
    return {"customer": customer}


@router.get("/address/{id}")
def get_address_by_id(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM address WHERE address.id = %s", (id,))
    address = cursor.fetchall()
    cursor.close()
    return {"address": address}


@router.post("/{id}/address/", status_code=201)
async def create_address(
    id,
    request: Request,
    conn=Depends(get_db_conn)
) -> Any: 
    body = await request.json()
    print("aquiiiiii ", body)
    print("id ", id)
    cursor = conn.cursor()
    address_id = uuid4()
    date_now = datetime.now()

    query = """
        INSERT INTO address (id, created_at, updated_at, state, city, complement, neighborhood, customer_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        str(address_id),
        date_now,
        date_now,
        body["state"],
        body["city"],
        body.get("complement"),
        body["neighborhood"],
        str(id)
    )
            
    body["address_id"] = address_id
    body["created_at"] = date_now
    body["updated_at"] = date_now
    body["customer_id"] = id
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    return body

@router.get("/{id}/address/")
def read_customer_adresses(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()
    cursor.execute("SELECT a.* FROM address a join customer c on a.customer_id = c.id WHERE c.id = (%s)", (id, ))
    addresses = cursor.fetchall()
    cursor.close()
    return {"addresses": addresses}


@router.post("/", status_code=201)
async def create_customer(body: Request, conn=Depends(get_db_conn)) -> Any:
    body = await body.json()
    cursor = conn.cursor()
    customer_id = uuid4()
    date_now = datetime.now()
    cursor.execute(
        "INSERT INTO CUSTOMER (id, name, email, password, phone, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (str(customer_id), body["name"], body["email"], encrypt_data(body["password"]), body["phone"], date_now, date_now)
    )
    conn.commit()
    cursor.close()
    body["id"] = customer_id
    body["updated_at"] = date_now
    body["created_at"] = date_now
    return body


@router.delete("/{id}/")
def delete_customer(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()

    cursor.execute("DELETE FROM customer WHERE id = %s", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        raise HTTPException(status_code=404, detail="Customer not found")

    cursor.close()
    return {"message": "Customer deleted successfully"}


@router.delete("/address/{id}/")
def delete_address(id, conn=Depends(get_db_conn)) -> Any:
    cursor = conn.cursor()

    cursor.execute("DELETE FROM address WHERE id = (%s)", (str(id),))
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        raise HTTPException(status_code=404, detail="Address not found")

    cursor.close()
    return {"message": "Address deleted successfully"}


@router.patch("/{id}/")
async def update_customer(id, customer: Request, conn=Depends(get_db_conn)):
    cursor = conn.cursor()
    customer = await customer.json()
    fields = []
    values = []

    if customer.get("name"):
        fields.append("name = %s")
        values.append(customer["name"])

    if customer.get("email"):
        fields.append("email = %s")
        values.append(customer["email"])

    if customer.get("phone"):
        fields.append("phone = %s")
        values.append(customer["phone"])

    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    values.append(str(id))   

    query = f"UPDATE customer SET {', '.join(fields)} WHERE id = %s"
    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        raise HTTPException(status_code=404, detail="Customer not found")

    cursor.close()
    return {"message": "Customer updated successfully"}


@router.post("/login/")
async def login(customer_request: Request, conn=Depends(get_db_conn)):
    customer_request = await customer_request.json()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer.email = %s", (customer_request["username"],))
    customer = cursor.fetchone()    
    cursor.close()
    stored_password_hash = customer[6]
    
    provided_password_hash = encrypt_data(customer_request["password"])
    if (not stored_password_hash) or (provided_password_hash != stored_password_hash): 
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    return {"access_token": TOKEN, "token_type": "bearer"}
        

@router.patch("/address/{id}/")
async def update_address(id, address: Request, conn=Depends(get_db_conn)):
    address = await address.json()
    cursor = conn.cursor()

    fields = []
    values = []

    if address.get("state"):
        fields.append("state = %s")
        values.append(address["state"])

    if address.get("city"):
        fields.append("city = %s")
        values.append(address["city"])

    if address.get("complement"):
        fields.append("complement = %s")
        values.append(address["complement"])

    if address.get("neighborhood"):
        fields.append("neighborhood = %s")
        values.append(address["neighborhood"])


    if not fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    values.append(str(id))   

    query = f"UPDATE address SET {', '.join(fields)} WHERE id = %s"

    cursor.execute(query, values)
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        raise HTTPException(status_code=404, detail="Address not found")

    cursor.close()
    return {"message": "Address updated successfully"}


@router.patch("/password/{id}")
async def update_password(
    id,
    password_request: Request,
    conn=Depends(get_db_conn),     
):
    password_request = await password_request.json()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer WHERE customer.id = (%s)", (str(id), ))
    customer = cursor.fetchone()
    print(customer)
    cursor.close()
    password_hashed = encrypt_data(password_request["new_password"])
    if(customer[6] != encrypt_data(password_request["current_password"])):
        raise HTTPException(
            status_code=400, 
            detail="Incorrect Password"
        )
    
    if(customer[6] == password_hashed):
        raise HTTPException(
            status_code=400, 
            detail="New password cannot be the same"
        )

    customer_service.update_password(conn, password_hashed, id) 
    return { "message": "Password updated successfully"}