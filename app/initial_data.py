from app.core.db import get_db_conn
def create_address(): 
    query = """
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

def create_customer(): 
    query = """
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    CREATE TABLE IF NOT exists teste(
        id uuid PRIMARY KEY DEFAULT uuid_generate_v4(), 
        name VARCHAR(255) not null, 
        phone VARCHAR(11) not null, 
        email VARCHAR(255) UNIQUE NOT NULL, 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """

def initialize_db(): 
    pass

if __name__ == "__main__": 
    initialize_db()