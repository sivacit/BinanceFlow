from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

DATABASE_URL = "postgresql://admin:quest@172.18.0.1:8812/qdb"

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

@app.get("/data")
def get_data():
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed"}

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BTCUSDT_1h_data LIMIT 5;")  # Update with correct table name
    data = cursor.fetchall()
    conn.close()
    return {"data": data}
