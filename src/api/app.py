from fastapi import FastAPI, Query
import psycopg2
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to access backend API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection details
DB_URL = "postgresql://admin:quest@172.18.0.1:8812/qdb"

# Function to connect to QuestDB and fetch data with optional parameters
def fetch_data(query, params=None):
    try:
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        return {"error": str(e)}

# Fetch actual BTC data
@app.get("/actual-data")
async def get_data():
    query = """
    SELECT date as timestamp, close FROM BTCUSDT_1h_data.csv ORDER BY timestamp ASC
    """
    rows = fetch_data(query)
    
    if isinstance(rows, dict):  # Error occurred
        return rows
    
    data = [{"timestamp": str(row[0]), "actual_price": row[1]} for row in rows]
    return data

# Fetch predicted BTC data
@app.get("/prediction-data")
async def get_prediction_data():
    query = """
    SELECT "Date" as timestamp, Predictions as predicted_price FROM valid_predictions.csv ORDER BY timestamp ASC
    """
    rows = fetch_data(query)
    
    if isinstance(rows, dict):  # Error occurred
        return rows
    
    data = [{"timestamp": str(row[0]), "predicted_price": row[1]} for row in rows]
    return data

# Fetch candlestick data
@app.get("/candlestick-data")
async def get_candlestick_data():
    query = """
    SELECT date as timestamp, open, high, low, close
    FROM BTCUSDT_1h_data.csv
    ORDER BY timestamp ASC
    """
    rows = fetch_data(query)
    
    if isinstance(rows, dict):  # Error occurred
        return rows
    
    data = [
        {
            "timestamp": str(row[0]),
            "open": row[1],
            "high": row[2],
            "low": row[3],
            "close": row[4],
        }
        for row in rows
    ]
    return data

# Fetch filtered actual BTC data
@app.get("/filtered-actual-data")
async def get_filtered_actual_data(
    start_date: str = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(None, description="End date in YYYY-MM-DD format")
):
    # If no filter is provided, fetch all data
    if not start_date or not end_date:
        query = """
        SELECT date as timestamp, close, high, low, open 
        FROM BTCUSDT_1h_data.csv
        ORDER BY date ASC
        """
        rows = fetch_data(query)
    else:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")

            if start_dt > end_dt:
                return {"error": "start_date cannot be greater than end_date"}

            query = """
            SELECT date as timestamp, close, high, low, open 
            FROM BTCUSDT_1h_data.csv
            WHERE date BETWEEN %s AND %s
            ORDER BY date ASC
            """
            rows = fetch_data(query, (start_date, end_date))

        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD."}

    if isinstance(rows, dict):  # Error occurred
        return rows
    
    data = [
        {
            "timestamp": str(row[0]),
            "close": row[1],
            "high": row[2],
            "low": row[3],
            "open": row[4]
        }
        for row in rows
    ]

    return data
