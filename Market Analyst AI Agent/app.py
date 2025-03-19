import requests
import json
import os
import gradio as gr
from transformers import pipeline

# Load API keys from environment variables
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
FRED_API_KEY = os.getenv("FRED_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

print("Alpha Vantage API Key:", ALPHA_VANTAGE_API_KEY)
print("FRED API Key:", FRED_API_KEY)
print("News API Key:", NEWS_API_KEY)

# Hugging Face summary model with facebook/bart-large-cnn
summary_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to get market news
def get_market_news():
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Error fetching market news: {e}")
        return []

# Function to get stock data from Alpha Vantage
def get_stock_data(symbol):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("Time Series (Daily)", {})
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching stock data: {e}")
        return {}

# Function to get economic data from FRED
def get_economic_data(series_id):
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={FRED_API_KEY}&file_type=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get("observations", [])
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching economic data: {e}")
        return []

# Function to generate executive summary
def generate_executive_summary(data):
    prompt = f"Summarize this market analysis:\n{data}"
    # Truncate the input to a maximum length of 1024 tokens
    truncated_prompt = prompt[:1024]
    summary = summary_pipeline(truncated_prompt, max_length=300, min_length=50, do_sample=False)[0]["summary_text"]
    return summary

# Gradio interface function
def market_analysis():
    print("Fetching Market News & Analyzing Sentiment...")
    market_news = get_market_news()
    stock_data = get_stock_data("AAPL")  # Example stock symbol
    economic_data = get_economic_data("GDP")  # Example economic series ID

    # Prepare data for summary
    summary_data = {
        "Market News": [article["title"] for article in market_news],
        "Stock Data": stock_data,
        "Economic Data": economic_data
    }
    
    print("Generating Executive Summary...")
    executive_summary = generate_executive_summary(json.dumps(summary_data, indent=2))

    print("Executive Summary generated successfully.")
    return executive_summary

# Create Gradio interface
iface = gr.Interface(
    fn=market_analysis,
    inputs=[],
    outputs="text",
    title="Market News Analysis",
    description="Fetches market news and generates an executive summary."
)

# Launch the interface
if __name__ == "__main__":
    iface.launch()