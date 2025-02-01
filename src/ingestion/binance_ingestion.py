import psycopg2
from binance import Client
import pandas as pd
from datetime import datetime

class BinanceToQuestDB:
    def __init__(self, api_key, api_secret, questdb_host, questdb_port, questdb_user, questdb_password, questdb_database):
        self.api_key = api_key
        self.api_secret = api_secret
        self.questdb_host = questdb_host
        self.questdb_port = questdb_port
        self.questdb_user = questdb_user
        self.questdb_password = questdb_password
        self.questdb_database = questdb_database

        # Initialize Binance client
        self.client = Client(self.api_key, self.api_secret, testnet=True)

    def fetch_historical_data(self, symbol, interval, start_time, end_time):
        """Fetch historical klines (candlestick data) from Binance."""
        klines = self.client.futures_klines(
            symbol=symbol,
            interval=interval,
            startTime=start_time,
            endTime=end_time,
            limit=1000
        )
        return klines

    def create_questdb_table(self, connection):
        """Create a table in QuestDB if it doesn't exist."""
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS btc_usdt (
                    tz TIMESTAMP,
                    open DOUBLE,
                    high DOUBLE,
                    low DOUBLE,
                    close DOUBLE,
                    volume DOUBLE
                ) TIMESTAMP(tz) PARTITION BY DAY;
            """)
            connection.commit()

    def insert_data_into_questdb(self, connection, data):
        """Insert data into QuestDB."""
        with connection.cursor() as cursor:
            for row in data:
                cursor.execute("""
                    INSERT INTO btc_usdt (tz, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s);
                """, row)
            connection.commit()

    def run(self, symbol, interval, start_time, end_time):
        """Main function to fetch data and insert into QuestDB."""
        # Fetch historical data from Binance
        klines = self.fetch_historical_data(symbol, interval, start_time, end_time)

        # Process klines into a DataFrame
        columns = [
            "Open Time", "Open", "High", "Low", "Close", "Volume",
            "Close Time", "Quote Asset Volume", "Number of Trades",
            "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"
        ]
        df = pd.DataFrame(klines, columns=columns)

        # Convert timestamps to datetime
        df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
        df["Close Time"] = pd.to_datetime(df["Close Time"], unit="ms")

        # Prepare data for QuestDB
        data = df[["Open Time", "Open", "High", "Low", "Close", "Volume"]].values.tolist()

        # Connect to QuestDB
        connection = psycopg2.connect(
            host=self.questdb_host,
            port=self.questdb_port,
            user=self.questdb_user,
            password=self.questdb_password,
            database=self.questdb_database
        )

        try:
            # Create table if it doesn't exist
            self.create_questdb_table(connection)

            # Insert data into QuestDB
            self.insert_data_into_questdb(connection, data)
            print("Data inserted successfully into QuestDB!")
        finally:
            # Close the connection
            connection.close()


if __name__ == "__main__":
    # Configuration
    API_KEY = "TY78itdlqqk5udyuWp05ZIKmZDhVEJEbJH8Mm68cUZFV81N2dWiCwf3hDD0bTLg5"
    API_SECRET = "h1QJsFtCdo7OWq7C7RZilXgzUtdQckCDjfwfcIaaHiZh6TTwFZx2i5Xxqrfxegot"
    QUESTDB_HOST = "localhost"
    QUESTDB_PORT = 8812
    QUESTDB_USER = "admin"
    QUESTDB_PASSWORD = "quest"
    QUESTDB_DATABASE = "qdb1"

    # Initialize and run the pipeline
    pipeline = BinanceToQuestDB(
        api_key=API_KEY,
        api_secret=API_SECRET,
        questdb_host=QUESTDB_HOST,
        questdb_port=QUESTDB_PORT,
        questdb_user=QUESTDB_USER,
        questdb_password=QUESTDB_PASSWORD,
        questdb_database=QUESTDB_DATABASE
    )

    # Define parameters
    symbol = "BTCUSDT"
    interval = Client.KLINE_INTERVAL_1HOUR  # 1-hour interval
    start_time = int(datetime(2023, 1, 1).timestamp() * 1000)  # Start time in milliseconds
    end_time = int(datetime(2023, 10, 1).timestamp() * 1000)  # End time in milliseconds

    # Run the pipeline
    pipeline.run(symbol, interval, start_time, end_time)