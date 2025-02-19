from fastapi import FastAPI
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

# Function to connect to QuestDB and fetch data
def fetch_data(query):
    try:
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        return {"error": str(e)}

@app.get("/actual-data")
async def get_data():
    query = """
    SELECT date as timestamp, close, low, high, open FROM BTCUSDT_1h_data.csv ORDER BY "timestamp" ASC
    """  # Removed .csv from table name
    rows = fetch_data(query)
    
    if isinstance(rows, dict):  # Error occurred
        return rows
    
    data = []
    for row in rows:
        try:
            # Ensure timestamp is in correct format
            timestamp = row[0]
            if isinstance(timestamp, datetime):
                timestamp = timestamp.isoformat()
            else:
                timestamp = str(timestamp)  # Convert to string if not datetime
            
            data.append({
                "timestamp": timestamp,
                "actual_price": row[1]
            })
        except Exception as e:
            print(f"Error parsing row {row}: {e}")

    return data

@app.get("/prediction-data")
async def get_prediction_data():
    query = """
    SELECT * FROM valid_predictions.csv ORDER BY "Date" ASC
    """  # Removed .csv from table name
    rows = fetch_data(query)
    
    if isinstance(rows, dict):  # Error occurred
        return rows
    
    data = []
    for row in rows:
        try:
            # Ensure timestamp is in correct format
            timestamp = row[0]
            if isinstance(timestamp, datetime):
                timestamp = timestamp.isoformat()
            else:
                timestamp = str(timestamp)  # Convert to string if not datetime
            
            data.append({
                "timestamp": timestamp,
                "predicted_price": row[1]
            })
        except Exception as e:
            print(f"Error parsing row {row}: {e}")

    return data

@app.get("/candlestick-data")
async def get_candlestick_data():
    query = """
    SELECT date as timestamp, open, high, low, close,
    FROM BTCUSDT_1h_data.csv
    ORDER BY "timestamp" ASC
    """  # Fetch timestamp, open, high, low, close, volume
    rows = fetch_data(query)
    
    if isinstance(rows, dict):  # Error occurred
        return rows
    
    data = []
    for row in rows:
        try:
            # Ensure timestamp is in correct format
            timestamp = row[0]
            if isinstance(timestamp, datetime):
                timestamp = timestamp.isoformat()
            else:
                timestamp = str(timestamp)  # Convert to string if not datetime
            
            data.append({
                "timestamp": timestamp,
                "open": row[1],
                "high": row[2],
                "low": row[3],
                "close": row[4],
            })
        except Exception as e:
            print(f"Error parsing row {row}: {e}")

    return data