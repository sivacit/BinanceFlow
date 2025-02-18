import requests
import pandas as pd
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional

# API Endpoint
ACTUAL_DATA_URL = "http://127.0.0.1:8000/questdb-data"
PREDICTION_TABLE = "future_btc_predictions"
QUESTDB_CONNECTION = "postgresql://admin:quest@172.18.0.1:8812/qdb"

# Fetch actual BTC data
response = requests.get(ACTUAL_DATA_URL)
if response.status_code != 200:
    print(f"❌ Failed to fetch data: {response.status_code}")
    exit()

data_raw = pd.DataFrame(response.json())

# Extract nested JSON data
data = pd.json_normalize(data_raw['data'])
data['timestamp'] = pd.to_datetime(data['timestamp'])
data.set_index('timestamp', inplace=True)

# Select relevant columns
features = ['open', 'high', 'low', 'close', 'volume']
data = data[features]

# Feature Engineering: Add SMA and RSI
data['SMA_10'] = data['close'].rolling(window=10).mean()
data['RSI'] = 100 - (100 / (1 + (data['close'].diff().clip(lower=0).rolling(14).mean() /
                                 -data['close'].diff().clip(upper=0).rolling(14).mean())))
data.dropna(inplace=True)  # Remove NaN values caused by rolling calculations

# Normalize features separately
scalers = {}
for col in data.columns:
    scalers[col] = MinMaxScaler(feature_range=(0, 1))
    data[col] = scalers[col].fit_transform(data[[col]])

# Define function for multi-step sequence creation
def create_sequences(data, seq_length, future_steps):
    X, y = [], []
    for i in range(len(data) - seq_length - future_steps):
        X.append(data.iloc[i:i+seq_length].values)  # Past sequence
        y.append(data.iloc[i+seq_length:i+seq_length+future_steps]['close'].values)  # Predict future close prices
    return np.array(X), np.array(y)

SEQ_LENGTH = 50   # Use past 50 hours
FUTURE_STEPS = 168  # Predict next 7 days (168 hours)

X, y = create_sequences(data, SEQ_LENGTH, FUTURE_STEPS)

# Split into training and test sets
split = int(len(X) * 0.8)
X_train, X_test = X[:split], X[split:]
y_train, y_test = y[:split], y[split:]

# Build Improved LSTM Model
model = Sequential([
    Bidirectional(LSTM(128, return_sequences=True, input_shape=(SEQ_LENGTH, X.shape[2]))),
    Dropout(0.3),
    Bidirectional(LSTM(128, return_sequences=False)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dense(FUTURE_STEPS)  # Predicting 168 future values (7 days)
])

model.compile(optimizer='adam', loss=tf.keras.losses.Huber())

# Train model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# Predict future 7 days using the last available sequence
last_sequence = data.iloc[-SEQ_LENGTH:].values.reshape(1, SEQ_LENGTH, X.shape[2])
future_predictions = model.predict(last_sequence)[0]

# Inverse scale the predictions
future_predictions_rescaled = scalers['close'].inverse_transform(
    future_predictions.reshape(-1, 1)).flatten()

# Create future timestamps
future_dates = pd.date_range(start=data.index[-1], periods=FUTURE_STEPS + 1, freq="H")[1:]

# Prepare forecast DataFrame
forecast_df = pd.DataFrame({'ds': future_dates, 'yhat': future_predictions_rescaled})

# Insert predictions into QuestDB
try:
    conn = psycopg2.connect(QUESTDB_CONNECTION)
    cursor = conn.cursor()
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {PREDICTION_TABLE} (
        date TIMESTAMP,
        prediction_price DOUBLE PRECISION
    ) TIMESTAMP(date);
    """)

    for _, row in forecast_df.iterrows():
        cursor.execute(
            f"INSERT INTO {PREDICTION_TABLE} (date, prediction_price) VALUES (%s, %s);",
            (row['ds'], row['yhat'])
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ 7-day predictions successfully stored in QuestDB!")

except Exception as e:
    print(f"❌ Error inserting predictions into QuestDB: {e}")

# Plot actual vs predicted
plt.figure(figsize=(12, 6))
plt.plot(future_dates, future_predictions_rescaled, label="Predicted", color="red", linestyle="dashed")
plt.legend()
plt.xlabel("Date")
plt.ylabel("BTC Price")
plt.title("BTC Price Prediction (Next 7 Days)")
plt.grid(True)
plt.show()
