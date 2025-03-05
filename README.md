# Crypto-Historical-Data-Retrieval

Project Overview: Using the Binance API for Cryptocurrency Analysis
Binance API Selection
The Binance API was selected for this project because it provides extensive access to
cryptocurrency data, covering over 300 trading pairs across platforms such as BTC/USDT,
ETH/USDT, BNB/BTC, etc. Key features include:
• Time Intervals Supported
Binance allows data retrieval at multiple intervals:
o Daily (1d), Hourly (1h), and Weekly (1w)
o Additional granular intervals: 1m (minute), 3m, 5m, 15m, 30m
o Larger intervals: 4h, 12h, and Monthly (1M)

API Key and Secret Setup
To ensure security, obtain a Binance API Key and Secret, and store them in a .env file. This
allows them to be securely loaded into the fetch_crypto_data.py script for data retrieval.

Script Explanation: fetch_crypto_data.py
This script includes the following functions:
1. convert_pair(pair)
o Converts cryptocurrency pairs from "BTC/USD" format to Binance’s required
format, "BTCUSDT."

2. fetch_crypto_data(crypto_pair, start_date)
o Fetches historical cryptocurrency data from Binance.
o Accepts a cryptocurrency pair and a start date as inputs.
o Converts the start date (in "YYYY-MM-DD" format) into a Unix timestamp
(milliseconds) as required by the Binance API.
o Returns a DataFrame containing Date, Open, High, Low, and Close prices.
o Uses Binance’s daily candlestick data for analysis.
3. calculate_metrics(data, variable1=7, variable2=5)
o Calculates various trading metrics with two customizable time periods:
▪ variable1: Look-back period (default 7 days)
▪ variable2: Look-forward period (default 5 days)
o Computes:
▪ Historical highs and lows

▪ Days since last high/low
▪ Percentage differences from highs/lows
▪ Future price movements
4. export_to_excel(data, filename)
o Exports the resulting DataFrame to an Excel file for easy access and further
analysis.

Script Explanation: ml_model.py
The ml_model.py script imports the fetch_crypto_data.py module to directly retrieve
historical data and calculated metrics for model training and testing. Users can specify a
cryptocurrency pair and start date to dynamically retrieve data. The model has two key
parameters:
• Variable1: Defines the number of days for input data.
• Variable2: Specifies the forecast period.
Data is split into an 80% training set and a 20% testing set. The model uses Random Forest
Regression for accurate price predictions.
Accuracy Metrics
• Mean Squared Error (MSE): 2.76
• Mean Absolute Error (MAE): 0.81
These indicate strong predictive performance, with absolute prediction errors
averaging below 1%.
Output Predictions:
• Percentage difference from future high prices
• Percentage difference from future low prices
Unique Strengths
• Supports multiple cryptocurrency pairs
• Balanced approach using both high and low prices
• Robust error handling for missing data
• Reproducible results with fixed random states
• Flexible timeframe adjustments
This setup provides a scalable, dynamic, and reliable approach for cryptocurrency data
analysis and price prediction using Binance’s comprehensive API data.
