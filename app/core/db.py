import psycopg2
from fastapi import Depends
from app.core.settings import Settings

def get_db_conn(settings: Settings = Depends(Settings)):
    conn = psycopg2.connect(
        dbname="customer_db",
        user="moretti-customer", 
        password="moretti",
        host="localhost",
        port="5432"
    )

    try:
        yield conn
    finally:
        conn.close()
