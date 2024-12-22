import psycopg2
from dotenv import load_dotenv
import os

from financial_analysis_backend.database import Database


if __name__ == "__main__":
    load_dotenv()
    CONNECTION_STRING = os.getenv("DATABASE_CONNECTION_STRING")
    with psycopg2.connect(CONNECTION_STRING) as conn:
        database = Database(conn)
        database.create_dataset_table()
