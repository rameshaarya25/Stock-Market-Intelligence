import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Stock Market Intelligence Platform")




stock_name = st.selectbox(
    "Select Stock",
    ["Reliance", "TCS", "Infosys", "HDFC Bank"]
)




stock_map = {
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS"
}

ticker = stock_map[stock_name]

data = yf.Ticker(ticker).history(period="1y")
latest_price = data["Close"].iloc[-1]

st.metric(
    "Current Price",
    f"₹{latest_price:.2f}"
)
# Current values
current_price = data["Close"].iloc[-1]
previous_price = data["Close"].iloc[-2]

change_percent = ((current_price - previous_price) / previous_price) * 100

volume = data["Volume"].iloc[-1]

trend = "Bullish" if current_price > previous_price else "Bearish"



st.subheader(f"{stock_name} Stock Data")
st.dataframe(data.tail())

st.subheader("Closing Price Chart")
st.line_chart(data["Close"])
st.subheader("Analysis")

daily_return = (
    (data["Close"].iloc[-1] - data["Close"].iloc[-2])
    / data["Close"].iloc[-2]
) * 100

st.write(f"Daily Return: {daily_return:.2f}%")
st.subheader("50-Day Moving Average")

data["MA50"] = data["Close"].rolling(window=50).mean()

st.line_chart(data[["Close", "MA50"]])
st.subheader("200-Day Moving Average")

data["MA200"] = data["Close"].rolling(window=200).mean()

st.line_chart(data[["Close", "MA200"]])
latest_price = data["Close"].iloc[-1]
ma200 = data["MA200"].iloc[-1]



delta = data["Close"].diff()

gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()

rs = avg_gain / avg_loss

data["RSI"] = 100 - (100 / (1 + rs))
latest_rsi = data["RSI"].iloc[-1]

if latest_rsi > 70:
    status = "Overbought"
elif latest_rsi < 30:
    status = "Oversold"
else:
    status = "Neutral"

st.subheader("RSI Analysis")
st.metric("RSI", f"{latest_rsi:.2f}")
st.write("Status:", status)
# =========================
# VOLATILITY ANALYSIS
# =========================

# Calculate Daily Returns
data["Daily_Return"] = data["Close"].pct_change()

# Calculate Volatility (%)
volatility = data["Daily_Return"].std() * 100

# Determine Risk Level
if volatility < 1:
    vol_status = "Low"
elif volatility < 2:
    vol_status = "Medium"
else:
    vol_status = "High"

# Display Results
st.subheader("Volatility Analysis")

st.metric(
    label="Volatility (%)",
    value=f"{volatility:.2f}%"
)

# Risk Status
if vol_status == "Low":
    st.success(f"🟢 Low Volatility ({volatility:.2f}%)")

elif vol_status == "Medium":
    st.warning(f"🟡 Medium Volatility ({volatility:.2f}%)")

else:
    st.error(f"🔴 High Volatility ({volatility:.2f}%)")

# Daily Returns Chart
st.subheader("Daily Returns Trend")
st.line_chart(data["Daily_Return"])

# Insights
st.subheader("Volatility Insight")

if volatility < 1:
    st.write(
        "The stock shows relatively stable price movement with lower risk and smaller day-to-day fluctuations."
    )

elif volatility < 2:
    st.write(
        "The stock exhibits moderate fluctuations and balanced risk characteristics."
    )

else:
    st.write(
        "The stock experiences significant price swings and may be considered high risk."
    )
    st.subheader("📊 Automated Insights")

insights = []

# Trend Insight
if latest_price > ma200:
    insights.append("📈 Bullish trend detected (Price above MA200)")
else:
    insights.append("📉 Bearish trend detected (Price below MA200)")

# RSI Insight
if latest_rsi > 70:
    insights.append("⚠ RSI indicates Overbought conditions")
elif latest_rsi < 30:
    insights.append("🟢 RSI indicates Oversold conditions")
else:
    insights.append("RSI is in a healthy range")

# Volatility Insight


# Monthly Performance
monthly_return = (
    (data["Close"].iloc[-1] - data["Close"].iloc[-30])
    / data["Close"].iloc[-30]
) * 100

if monthly_return > 0:
    insights.append(f"📈 Stock gained {monthly_return:.2f}% in the last month")
else:
    insights.append(f"📉 Stock lost {abs(monthly_return):.2f}% in the last month")

# Volume Insight
avg_volume = data["Volume"].mean()
latest_volume = data["Volume"].iloc[-1]

if latest_volume > avg_volume:
    insights.append(" Trading volume is above average")
else:
    insights.append(" Trading volume is below average")

# Display Insights
for insight in insights:
    st.write(insight)
st.header("MARKET STATUS")

st.write(f"Current Price: ₹{current_price:.2f}")
st.write(f"Today's Change: {change_percent:.2f}%")
st.write(f"Market Trend: {trend}")
st.write(f"Volume: {volume:,}")
