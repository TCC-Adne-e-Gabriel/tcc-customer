from app.core.db import get_db_connection
def create_tables(): 
    queries = (
        """ 
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE IF NOT exists customer(
            id uuid PRIMARY KEY DEFAULT uuid_generate_v4(), 
            name VARCHAR(255) not null, 
            phone VARCHAR(11) not null, 
            email VARCHAR(255) UNIQUE NOT NULL, 
            password VARCHAR(255) NOT NULL, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """, 
                """
        CREATE TABLE IF NOT EXISTS address (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            state VARCHAR(100) NOT NULL,
            city VARCHAR(100) NOT NULL,
            complement VARCHAR(255),
            neighborhood VARCHAR(100) NOT NULL,
            customer_id UUID NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            CONSTRAINT address_customer
                FOREIGN KEY (customer_id)
                REFERENCES customer(id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        );
        """
    )
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            for command in queries:
                cur.execute(command)
            conn.commit()

def initialize_db(): 
    create_tables()
