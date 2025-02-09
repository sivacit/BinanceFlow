import math
import pandas as pd
import numpy as np
import psycopg2
from psycopg2.extras import execute_values
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM

plt.style.use('fivethirtyeight')

# QuestDB Connection
DATABASE_URL = "postgresql://admin:quest@172.18.0.1:8812/qdb"

# Fetch Data from QuestDB
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
query = 'SELECT * FROM "BTCUSDT_1h_data.csv"'
df = pd.read_sql(query, conn)
cursor.close()
conn.close()

# Rename 'timestamp' column to 'Date'
df.rename(columns={'timestamp': 'Date'}, inplace=True)
df['Date'] = pd.to_datetime(df['Date'])

# Filter data within a specific date range
start_date = '2020-12-29'
end_date = '2025-01-31'
df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

# Visualize Close Price
plt.figure(figsize=(16, 8))
plt.title('Close Price History')
plt.plot(df['Date'], df['close'])
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize=18)
plt.show()

# Prepare Data for Training
data = df[['close']]
dataset = data.values
training_data_len = math.ceil(len(dataset) * 0.8)

# Scale the Data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)

# Create Training Data
train_data = scaled_data[0:training_data_len, :]
x_train, y_train = [], []

for i in range(60, len(train_data)):
    x_train.append(train_data[i - 60:i, 0])
    y_train.append(train_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# Build LSTM Model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

# Compile and Train Model
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, batch_size=1, epochs=1)

# Create Testing Data
test_data = scaled_data[training_data_len - 60:, :]
x_test, y_test = [], dataset[training_data_len:, :]

for i in range(60, len(test_data)):
    x_test.append(test_data[i - 60:i, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Predict Prices
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# Calculate RMSE
rmse = np.sqrt(np.mean((predictions - y_test) ** 2))
print(f"RMSE: {rmse}")

# Create Validation DataFrame
train = data[:training_data_len]
valid = data[training_data_len:].copy()
valid['Predictions'] = predictions

# Plot Actual vs Predicted Prices
plt.figure(figsize=(16, 8))
plt.title('Model Predictions')
plt.plot(train.index, train['close'])
plt.plot(valid.index, valid[['close', 'Predictions']])
plt.xlabel('Date', fontsize=18)
plt.ylabel('Close Price USD ($)', fontsize=18)
plt.legend(['Train', 'Actual', 'Predictions'], loc='lower right')
plt.xticks(rotation=45)
plt.show()

# Store Predictions in QuestDB
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create Predictions Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS btc_predictions (
        date TIMESTAMP,
        actual_price DOUBLE PRECISION,
        predicted_price DOUBLE PRECISION
    );
""")
conn.commit()

# Insert Predicted Data
prediction_data = list(zip(valid.index, valid['close'], valid['Predictions']))
insert_query = "INSERT INTO btc_predictions (date, actual_price, predicted_price) VALUES %s"
execute_values(cursor, insert_query, prediction_data)
conn.commit()

print("✅ Predicted data inserted into QuestDB!")

cursor.close()
conn.close()

# Predict Next Close Price
last_60_days = data[-60:].values
last_60_days_scaled = scaler.transform(last_60_days)

x_test = []
x_test.append(last_60_days_scaled)
x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

pred_price = model.predict(x_test)
pred_price = scaler.inverse_transform(pred_price)

print(f"Predicted Next Price: {pred_price[0][0]}")
