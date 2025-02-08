from fastapi import APIRouter
import database

router = APIRouter()

# Fetch the latest 100 BTC data entries
@router.get("/btc_data")
def get_btc_data():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BTCUSDT_1h_data ORDER BY timestamp DESC LIMIT 100")
    data = cursor.fetchall()
    conn.close()
    return {"btc_data": data}

# Fetch To-Do List items
@router.get("/todos")
def get_todos():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM todo_list")
    todos = cursor.fetchall()
    conn.close()
    return {"todos": todos}

# Combine To-Do List with latest BTC data
@router.get("/todo_with_btc")
def get_todo_with_btc():
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM todo_list")
    todos = cursor.fetchall()

    cursor.execute("SELECT * FROM BTCUSDT_1h_data ORDER BY timestamp DESC LIMIT 1")
    btc_data = cursor.fetchone()

    conn.close()

    return {"todos": todos, "latest_btc": btc_data}
