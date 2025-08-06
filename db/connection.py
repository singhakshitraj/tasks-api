import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
def connect_to_db():
    load_dotenv()
    connection=psycopg2.connect(
        host=os.environ.get('HOST'),
        port=os.environ.get('PORT'),
        user=os.environ.get('USER'),
        password=os.environ.get('PASSWORD'),
        dbname=os.environ.get('DB_NAME'),
        cursor_factory=RealDictCursor
    )
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()

