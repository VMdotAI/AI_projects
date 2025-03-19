import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load API keys from environment variables
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "your-alpha-vantage-api-key-here")
FRED_API_KEY = os.getenv("FRED_API_KEY", "your-fred-api-key-here")
SEC_API_KEY = os.getenv("SEC_API_KEY", "your-sec-api-key-here")

# Function to fetch stock market risk (Alpha Vantage)
def get_stock_risk(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "Time Series (Daily)" in data:
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index", dtype=float)
            df.index = pd.to_datetime(df.index)
            df.sort_index(inplace=True)
            
            df["daily_return"] = df["4. close"].pct_change()
            volatility = df["daily_return"].std()
            
            risk_score = "High" if volatility > 0.03 else "Medium" if volatility > 0.015 else "Low"
            
            return df, risk_score
        else:
            return None, "Unknown"
    
    except requests.exceptions.RequestException as e:
        return None, "Unknown"

# Function to fetch economic risk indicators from FRED
def get_fred_data(series_id):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"

    try:
        response = requests.get(url)
        data = response.json()
        observations = data.get("observations", [])
        
        if not observations:
            return "No economic data available."
        
        latest_data = observations[-1]
        return f"Latest GDP Data: {latest_data['value']} (Date: {latest_data['date']})"
    
    except requests.exceptions.RequestException as e:
        return "Error fetching economic data."

# Function to fetch SEC filings (Regulatory Risk)
def get_sec_filings(symbol):
    url = f"https://sec-api.io/api/v1/company-filings?token={SEC_API_KEY}&ticker={symbol}&type=10-K"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return ["SEC API Error. Try again later."]
        
        data = response.json()
        filings = data.get("filings", [])
        if not filings:
            return ["No recent filings found."]
        return filings[:5]

    except requests.exceptions.RequestException:
        return ["Error fetching SEC filings."]
    except requests.exceptions.JSONDecodeError:
        return ["Error decoding SEC filings."]

# Function to plot historical risk trend
def plot_risk_trend(df, symbol):
    if df is not None and "daily_return" in df.columns:
        plt.figure(figsize=(10, 5))
        plt.plot(df.index, df["daily_return"], label="Daily Return Volatility", color="blue")
        plt.axhline(y=0, color='black', linestyle='--', linewidth=0.5)
        plt.legend()
        plt.title(f"Historical Risk Trend for {symbol}")
        plt.xlabel("Date")
        plt.ylabel("Daily Return Volatility")
        st.pyplot(plt)
    else:
        st.write("⚠️ Not enough data to display risk trends.")

# Streamlit UI
st.title("🛡️ Risk & Compliance Agent")
st.write("Monitor financial, regulatory, and cybersecurity risks.")

# Stock Market Risk
symbol = st.text_input("🔍 Enter Stock Symbol", value="AAPL")

if symbol:
    # Fetch and display stock risk
    df, risk_score = get_stock_risk(symbol)
    
    st.subheader("📉 Market & Economic Risk")
    st.write(f"**Risk Score:** {risk_score}")
    
    # Fetch and display economic data
    st.subheader("📊 Economic Indicators")
    st.write(get_fred_data("GDP"))
    
    # Fetch and display SEC filings
    st.subheader("📜 SEC Filings (Regulatory Risk)")
    filings = get_sec_filings(symbol)
    for filing in filings:
        if isinstance(filing, dict):
            st.write(f"📄 [{filing['title']}]({filing['link']}) - {filing['date']}")
        else:
            st.write(filing)

    # Plot Historical Risk Trend
    st.subheader("📊 Historical Risk Trends")
    plot_risk_trend(df, symbol)

st.success("✅ Risk & Compliance Report Updated!")