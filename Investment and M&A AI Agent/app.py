import streamlit as st
import requests
import os

# Load API keys from Hugging Face secrets
ALPHA_VANTAGE_API_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"]
FRED_API_KEY = st.secrets["FRED_API_KEY"]
FMP_API_KEY = st.secrets["FMP_API_KEY"]

# Function to fetch company fundamentals
def get_fundamental_data(symbol):
    try:
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return {}

# Function to get economic data from FRED
def get_economic_data(series_id):
    try:
        url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get("observations", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []

# Function to get company data from Financial Modeling Prep
def get_fmp_data(symbol):
    try:
        url = f"https://financialmodelingprep.com/api/v3/profile/{symbol}?apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()[0] if response.json() else {}
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return {}

# Streamlit UI
st.title("💼 Investment & M&A Agent")
st.markdown("AI-driven insights for strategic growth, M&A, and investments.")

symbol = st.text_input("🔍 Enter Stock Symbol", value="AAPL")

if symbol:
    st.subheader("📊 Company Financial Overview")
    fundamentals = get_fundamental_data(symbol)
    if fundamentals:
        st.write(f"**Name:** {fundamentals.get('Name', 'N/A')}")
        st.write(f"**Market Cap:** {fundamentals.get('MarketCapitalization', 'N/A')}")
        st.write(f"**Revenue:** {fundamentals.get('RevenueTTM', 'N/A')}")
        st.write(f"**Profit Margin:** {fundamentals.get('ProfitMargin', 'N/A')}")

    st.subheader("📉 Economic Indicators")
    indicators = ["GDP", "UNRATE", "CPIAUCSL"]
    for indicator in indicators:
        economic_data = get_economic_data(indicator)
        if economic_data:
            latest_data = economic_data[-1]
            st.write(f"**Latest {indicator}:** {latest_data['value']} (Date: {latest_data['date']})")

    st.subheader("💰 Funding & Investment Opportunities")
    company_data = get_fmp_data(symbol.lower())
    if company_data:
        st.write(f"**Company Name:** {company_data.get('companyName', 'N/A')}")
        st.write(f"**CEO:** {company_data.get('ceo', 'N/A')}")
        st.write(f"**Industry:** {company_data.get('industry', 'N/A')}")
        st.write(f"**Website:** {company_data.get('website', 'N/A')}")
    else:
        st.write("No recent funding data found.")

st.success("✅ Investment & M&A Report Generated!")