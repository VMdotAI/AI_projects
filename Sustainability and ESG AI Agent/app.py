import os
import requests
import streamlit as st
import matplotlib.pyplot as plt

# Load API key securely from environment variables
CARBON_INTERFACE_API_KEY = os.getenv("CARBON_INTERFACE_API_KEY")

# Function to get environmental data from Carbon Interface
def get_environmental_data(company_name):
    if not CARBON_INTERFACE_API_KEY:
        st.error("API key is missing. Please set the CARBON_INTERFACE_API_KEY environment variable.")
        return None

    url = f"https://www.carboninterface.com/api/v1/estimates?company={company_name}"
    headers = {
        "Authorization": f"Bearer {CARBON_INTERFACE_API_KEY}"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if "data" in data:
            return data["data"]
        else:
            st.error("No environmental data found for the given company.")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
    return None

# Function to extract environmental scores
def extract_environmental_scores(environmental_data):
    if not environmental_data:
        return None, None, None

    years = ["2021", "2022", "2023", "2024", "2025"]  # Example years
    env_scores = [environmental_data.get("carbon_emissions", "N/A")] * 5
    soc_scores = [environmental_data.get("carbon_efficiency", "N/A")] * 5
    gov_scores = [environmental_data.get("sustainability_rating", "N/A")] * 5

    return years, env_scores, soc_scores, gov_scores

# Function to plot historical environmental trends
def plot_environmental_trends(company_name, years, env_scores, soc_scores, gov_scores):
    plt.figure(figsize=(8, 4))
    plt.plot(years, env_scores, label="Carbon Emissions", marker="o", linestyle="--", color="green")
    plt.plot(years, soc_scores, label="Carbon Efficiency", marker="o", linestyle="--", color="blue")
    plt.plot(years, gov_scores, label="Sustainability Rating", marker="o", linestyle="--", color="red")

    plt.xlabel("Year")
    plt.ylabel("Score")
    plt.title(f"📈 Environmental Trends for {company_name}")
    plt.legend()
    plt.grid(True)

    st.pyplot(plt)

# Function to compare environmental data with competitors
def compare_with_competitors(company_name, competitors):
    competitor_scores = {}
    for comp in competitors:
        data = get_environmental_data(comp)
        if data:
            competitor_scores[comp] = {
                "Carbon Emissions": data.get("carbon_emissions", "N/A"),
                "Carbon Efficiency": data.get("carbon_efficiency", "N/A"),
                "Sustainability Rating": data.get("sustainability_rating", "N/A")
            }

    st.subheader(f"📊 Environmental Comparison: {company_name} vs Competitors")
    st.write("Comparison of environmental data across companies:")

    if competitor_scores:
        st.table(competitor_scores)
    else:
        st.write("No competitor data available.")

# Streamlit UI
st.title("🌱 Sustainability & ESG Agent")
st.write("Ensure AI-driven business strategies align with ESG goals.")

# Input for company name
company_name = st.text_input("🔍 Enter Company Name", value="Apple Inc.")

if company_name:
    environmental_data = get_environmental_data(company_name)
    
    st.subheader(f"📊 Environmental Data for {company_name}")

    if environmental_data:
        st.write(f"**Carbon Emissions:** {environmental_data.get('carbon_emissions', 'N/A')}")
        st.write(f"**Carbon Efficiency:** {environmental_data.get('carbon_efficiency', 'N/A')}")
        st.write(f"**Sustainability Rating:** {environmental_data.get('sustainability_rating', 'N/A')}")

        # Extract and display environmental trends
        years, env_scores, soc_scores, gov_scores = extract_environmental_scores(environmental_data)
        if years and env_scores and soc_scores and gov_scores:
            st.subheader("📈 Environmental Historical Trends")
            plot_environmental_trends(company_name, years, env_scores, soc_scores, gov_scores)

        # Compare with competitors (example: Microsoft, Tesla, Google)
        competitors = ["Microsoft", "Tesla", "Google"]
        compare_with_competitors(company_name, competitors)

    else:
        st.write("No environmental data found.")

st.success("✅ Environmental Report Updated!")