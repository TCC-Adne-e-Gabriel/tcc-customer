from app.models.customer import Customer
from sqlmodel import Session, select
from uuid import UUID

class CustomerService():
    def get_customer(self, conn, customer_id): 
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customer WHERE customer.id = %s", (customer_id,))
        customer = cursor.fetchone()    
        cursor.close()
        return customer
    
    def update_password(self, conn, password, id): 
        cursor = conn.cursor()
        query = "UPDATE customer SET password = %s WHERE id = %s RETURNING id, name, email, phone, created_at, updated_at"
        cursor.execute(query, (password, id))
        current_customer = cursor.fetchone()
        conn.commit()
        return current_customer
