import os
import requests
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Load API Key from Hugging Face Secrets
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Function to simulate operational efficiency scoring
def get_efficiency_score():
    """Simulated AI-driven efficiency score (0 to 100)"""
    return np.random.randint(50, 95)

# Function to provide workflow optimization suggestions
def suggest_optimizations():
    suggestions = [
        "🚀 Automate repetitive tasks with AI tools.",
        "📊 Use data-driven insights to optimize resource allocation.",
        "🔄 Implement real-time performance tracking.",
        "📉 Reduce operational costs by switching to cloud solutions.",
        "🔧 Improve workflow automation with process mining techniques."
    ]
    return np.random.choice(suggestions, 3, replace=False)

# Function to fetch industry efficiency benchmarks (Example API call)
def get_industry_benchmark():
    url = f"https://www.alphavantage.co/query?function=SECTOR&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("Rank B: Operating Margin %", {})
    return {}

# Function to get operational data for a specific company
def get_company_efficiency(symbol):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

# Function to visualize efficiency trend
def plot_efficiency_trend():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    efficiency_scores = np.random.randint(50, 95, len(months))  # Simulated data
    
    plt.figure(figsize=(8, 4))
    plt.plot(months, efficiency_scores, marker="o", linestyle="--", color="blue")
    plt.xlabel("Month")
    plt.ylabel("Efficiency Score")
    plt.title("📈 Operational Efficiency Over Time")
    plt.grid(True)

    st.pyplot(plt)

# Streamlit UI
st.title("⚙️ Operational Efficiency Agent")
st.write("Optimize AI-driven workflows, reduce costs, and enhance resource allocation.")

# User Input: Stock Symbol
symbol = st.text_input("🔍 Enter Company Stock Symbol (e.g., AAPL, TSLA, MSFT)", value="AAPL")

if symbol:
    # Generate Efficiency Score
    efficiency_score = get_efficiency_score()
    st.subheader(f"📊 Efficiency Score for {symbol}: {efficiency_score}/100")

    # Fetch Company Efficiency Data
    company_data = get_company_efficiency(symbol)
    if company_data:
        st.write(f"🏢 **Company Name:** {company_data.get('Name', 'N/A')}")
        st.write(f"💰 **Operating Margin:** {company_data.get('OperatingMarginTTM', 'N/A')}")
        st.write(f"📊 **Return on Assets:** {company_data.get('ReturnOnAssetsTTM', 'N/A')}")
        st.write(f"⚙️ **Return on Equity:** {company_data.get('ReturnOnEquityTTM', 'N/A')}")
    else:
        st.write("No company efficiency data available.")

    # Show Optimization Suggestions
    st.subheader("🔄 Workflow Optimization Suggestions")
    suggestions = suggest_optimizations()
    for suggestion in suggestions:
        st.write(suggestion)

    # Show Efficiency Trend
    st.subheader("📈 Efficiency Trend Over Time")
    plot_efficiency_trend()

    # Show Industry Benchmark Data
    st.subheader("🏭 Industry Benchmarking")
    industry_data = get_industry_benchmark()
    if industry_data:
        st.write("Comparison with Industry Operating Margins (%):")
        st.json(industry_data)
    else:
        st.write("No industry data available.")

    st.success("✅ Operational Efficiency Report Updated!")