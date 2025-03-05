import os
import pandas as pd
from binance.client import Client
from dotenv import load_dotenv
from datetime import datetime

# Load API keys from .env file
load_dotenv()
# Retrieve Binance API credentials from environment variables
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

# Initialize the Binance Client
client = Client(api_key, api_secret)

def convert_pair(pair):
    """
    Converts a crypto pair like 'BTC/USD' into the Binance format 'BTCUSDT'.

    Parameters:
    - pair: str, input pair in the format "BTC/USD".
    
    Returns:
    - str, converted pair in Binance format, e.g., "BTCUSDT".
    """
    return pair.replace("/", "").upper()

def fetch_crypto_data(crypto_pair, start_date):
    """
    Fetches daily historical data for a specified cryptocurrency pair from Binance.
    
    Parameters:
    - crypto_pair: The trading pair in format "BTC/USD".
    - start_date: The start date for data retrieval in "YYYY-MM-DD" format.
    
    Returns:
    - A pandas DataFrame containing Date, Open, High, Low, and Close prices.
    """
    # Convert crypto pair format for Binance API (e.g., "BTC/USD" -> "BTCUSDT")
    symbol = convert_pair(crypto_pair)
    
    # Convert start date to timestamp for Binance API
    start_timestamp = int(pd.to_datetime(start_date).timestamp() * 1000)

    # Retrieve historical klines/candlestick data from Binance API
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1DAY, start_timestamp)
    
    # Create a DataFrame from the retrieved data
    df = pd.DataFrame(klines, columns=[
        "Date", "Open", "High", "Low", "Close", "Volume", 
        "Close Time", "Quote Asset Volume", "Number of Trades", 
        "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"
    ])
    
    # Keep only necessary columns and format data types
    df["Date"] = pd.to_datetime(df["Date"], unit='ms')
    df["Open"] = df["Open"].astype(float)
    df["High"] = df["High"].astype(float)
    df["Low"] = df["Low"].astype(float)
    df["Close"] = df["Close"].astype(float)
    
    return df[["Date", "Open", "High", "Low", "Close"]]

# Example usage
# crypto_pair = "BTCUSDT"
# start_date = "2022-01-01"
# data = fetch_crypto_data(crypto_pair, start_date)
# print(data.head())



def calculate_metrics(data, variable1=7, variable2=5):
    """
    Calculates trading metrics for historical and future price movements.

    Parameters:
    - data: DataFrame containing historical price data.
    - variable1: Integer for look-back period (e.g., 7 days).
    - variable2: Integer for look-forward period (e.g., 5 days).

    Returns:
    - DataFrame with additional columns for calculated metrics.
    """
    # Calculate historical high and low prices over variable1 days
    data[f"High_Last_{variable1}_Days"] = data['High'].rolling(window=variable1).max()
    data[f"Low_Last_{variable1}_Days"] = data['Low'].rolling(window=variable1).min()

    # Days since last high/low
    data[f"Days_Since_High_Last_{variable1}_Days"] = (
        data['Date'] - data['Date'].where(data['High'] == data[f"High_Last_{variable1}_Days"]).ffill()
    ).dt.days
    data[f"Days_Since_Low_Last_{variable1}_Days"] = (
        data['Date'] - data['Date'].where(data['Low'] == data[f"Low_Last_{variable1}_Days"]).ffill()
    ).dt.days

    # Percentage differences from historical high/low
    data[f"%_Diff_From_High_Last_{variable1}_Days"] = (
        (data['Close'] - data[f"High_Last_{variable1}_Days"]) / data[f"High_Last_{variable1}_Days"]
    ) * 100
    data[f"%_Diff_From_Low_Last_{variable1}_Days"] = (
        (data['Close'] - data[f"Low_Last_{variable1}_Days"]) / data[f"Low_Last_{variable1}_Days"]
    ) * 100

    # Calculate future high and low prices over variable2 days
    data[f"High_Next_{variable2}_Days"] = data['High'].shift(-variable2).rolling(window=variable2).max()
    data[f"Low_Next_{variable2}_Days"] = data['Low'].shift(-variable2).rolling(window=variable2).min()

    # Percentage differences from future high/low
    data[f"%_Diff_From_High_Next_{variable2}_Days"] = (
        (data['Close'] - data[f"High_Next_{variable2}_Days"]) / data[f"High_Next_{variable2}_Days"]
    ) * 100
    data[f"%_Diff_From_Low_Next_{variable2}_Days"] = (
        (data['Close'] - data[f"Low_Next_{variable2}_Days"]) / data[f"Low_Next_{variable2}_Days"]
    ) * 100

    return data



def export_to_excel(data, filename="crypto_data.xlsx"):
    """
    Exports the DataFrame to an Excel file.

    Parameters:
    - data: The DataFrame containing the data.
    - filename: The name of the Excel file to save.
    """
    data.to_excel(filename, index=False)
    print(f"Data exported to {filename} successfully.")





if __name__ == "__main__":
    # Get user inputs for crypto pair and start date
    crypto_pair = input("Enter the crypto pair (e.g., BTC/USD as BTCUSDT): ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")

    # Step 1: Fetch data for the user-specified pair and start date
    data = fetch_crypto_data(crypto_pair, start_date)
    print("Data retrieved successfully!")

    # Step 2: Calculate metrics with specified look-back and look-forward periods
    variable1 = 7  # Change this if a different period is desired
    variable2 = 5  # Change this if a different period is desired
    metrics_data = calculate_metrics(data, variable1, variable2)
    print("Metrics calculated successfully!")

    # Step 3: Export the data to Excel
    export_to_excel(metrics_data, f"{crypto_pair.replace('/', '_')}_Historical_Data.xlsx")
    print("Data exported to Excel successfully!")
