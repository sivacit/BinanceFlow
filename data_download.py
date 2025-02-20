import requests
import pandas as pd
import time

# Binance API URL
BINANCE_API_URL = "https://api.binance.com/api/v3/klines"

# Parameters
symbol = "BTCUSDT"
interval = "1h"  # Change to "1d", "15m", etc., as needed
start_time = int(pd.Timestamp("2020-01-01").timestamp() * 1000)  # Start from 2020-01-01
end_time = int(pd.Timestamp.now().timestamp() * 1000)  # Current timestamp

all_data = []
limit = 1000  # Max limit per request

print("Fetching BTC/USDT data from Binance...")

while start_time < end_time:
    params = {
        "symbol": symbol,
        "interval": interval,
        "startTime": start_time,
        "limit": limit
    }
    
    response = requests.get(BINANCE_API_URL, params=params)
    data = response.json()
    
    if not data:
        break  # Stop if no data is returned

    all_data.extend(data)
    
    # Update start_time to fetch the next batch
    start_time = data[-1][0] + 1
    
    print(f"Fetched {len(data)} records, moving to next batch...")
    time.sleep(1)  # To avoid rate limits

# Convert to DataFrame and keep only required columns
df = pd.DataFrame(all_data, columns=[
    "timestamp", "open", "high", "low", "close", "volume",
    "_", "_", "_", "_", "_", "_"
])

# Keep only necessary columns and convert timestamp
df = df[["timestamp", "open", "high", "low", "close", "volume"]]
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
df.rename(columns={"timestamp": "date"}, inplace=True)

# Save to CSV
df.to_csv("BTCUSDT_1h_2020_present.csv", index=False)
print("✅ Data saved as BTCUSDT_1h_2020_present.csv")
