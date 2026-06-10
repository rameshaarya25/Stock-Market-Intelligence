import yfinance as yf
import pandas as pd

# Stock symbol
stock = yf.Ticker("RELIANCE.NS")



# Get 1 year of historical data
data = stock.history(period="1y")

# Save to CSV
data.to_csv("data/stock_data.csv")

print("Data saved successfully!")
print(data.head())