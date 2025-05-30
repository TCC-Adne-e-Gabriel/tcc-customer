import psycopg2
from fastapi import Depends
from settings import Settings

def get_db_conn(settings: Settings = Depends(Settings)):
    conn = psycopg2.connect(
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        host=settings.db_host,
        port=settings.db_port
    )
    try:
        yield conn
    finally:
        conn.close()
