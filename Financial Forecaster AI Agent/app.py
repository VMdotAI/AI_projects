import requests
import pandas as pd
import os
import gradio as gr
from transformers import pipeline

# Load API keys from environment variables
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "your_default_key_here")

# === Fetch Free Stock Price from Alpha Vantage ===
def get_stock_price(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=compact"
    response = requests.get(url)
    data = response.json()
    if "Time Series (Daily)" in data:
        latest_date = sorted(data["Time Series (Daily)"].keys())[-1]
        latest_price = float(data["Time Series (Daily)"][latest_date]["4. close"])
        return latest_price
    return "Error: Invalid Symbol or API Limit Reached"

# === Simulated Revenue and Cost Data ===
revenue_data = [100000, 120000, 135000, 150000, 170000]  # Mock revenue values
cost_data = [50000, 55000, 60000, 65000, 70000]  # Mock cost values
years = [2020, 2021, 2022, 2023, 2024]

df = pd.DataFrame({"year": years, "revenue": revenue_data, "costs": cost_data})
df["ai_savings"] = df["revenue"] * 0.05  # AI-driven savings estimate (5% of revenue)

# === Generate Executive Summary ===
summary_pipeline = pipeline("text-generation", model="facebook/opt-350m", device=-1)  # Use smaller model

def generate_summary():
    summary_prompt = f"""
    Company Financial Forecast:
    - Projected revenue for next year: ${df['revenue'].iloc[-1]}
    - Estimated AI-driven cost savings: ${df['ai_savings'].iloc[-1]}

    """
    summary_text = summary_pipeline(summary_prompt, max_new_tokens=100)[0]['generated_text']
    return summary_text

# === Gradio Interface ===
def gradio_app(stock_ticker):
    stock_price = get_stock_price(stock_ticker)
    summary = generate_summary()
    return f"Latest {stock_ticker} Price: ${stock_price}", summary

iface = gr.Interface(
    fn=gradio_app,
    inputs=[gr.Textbox(label="Enter Stock Ticker", value="AAPL")],
    outputs=[gr.Textbox(label="Stock Price"), gr.Textbox(label="Executive Summary")],
    title="Financial Forecast & AI Summary",
    description="Get the latest stock price and a financial forecast summary."
)

# === Run Gradio App ===
if __name__ == "__main__":
    iface.launch()
