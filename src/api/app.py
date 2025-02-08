from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Allow frontend (Vue.js) to access FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection settings
DATABASE_URL = "postgresql://admin:quest@172.18.0.1:8812/qdb"

def get_db_connection():
    """Establish a connection to the QuestDB database."""
    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

@app.get("/questdb-data")
def get_data(
    start_date: str = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End date (YYYY-MM-DD)")
):
    """Fetch data from QuestDB within a date range."""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = conn.cursor()

        # Construct SQL query based on date filters
        query = 'SELECT * FROM "BTCUSDT_1h_data.csv"'
        conditions = []

        if start_date:
            conditions.append(f"timestamp >= '{start_date}'")
        if end_date:
            conditions.append(f"timestamp <= '{end_date}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY timestamp ASC;"  # Sorting by timestamp

        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return {"data": data}
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch data from QuestDB")

# Root endpoint for testing
@app.get("/")
def root():
    return {"message": "FastAPI server is running"}