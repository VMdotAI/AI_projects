import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import joblib

# 🎯 **Customer Insights Agent**
st.title("📊 Customer Insights Agent")
st.write("Analyze customer sentiment, market segmentation, and behavioral trends.")

# 📤 **Step 1: Upload Customer Data**
uploaded_file = st.file_uploader("Upload Customer Data (CSV)", type=["csv"])

if uploaded_file:
    # Load dataset
    df = pd.read_csv(uploaded_file)
    st.write("📊 Sample Data Preview:", df.head())

    # ✅ **Step 2: Sentiment Analysis on Customer Reviews**
    if "review" in df.columns:
        st.subheader("💬 Sentiment Analysis on Customer Reviews")
        df["Sentiment"] = df["review"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        df["Sentiment Label"] = df["Sentiment"].apply(lambda x: "Positive" if x > 0.2 else ("Negative" if x < -0.2 else "Neutral"))

        # Show sentiment distribution
        sentiment_counts = df["Sentiment Label"].value_counts()
        st.bar_chart(sentiment_counts)

    # ✅ **Step 3: Market Segmentation (K-Means Clustering)**
    st.subheader("📌 Market Segmentation")
    features = ["age", "income", "spending_score"]  # Modify based on dataset
    if all(col in df.columns for col in features):
        X = df[features]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Apply K-Means clustering
        kmeans = KMeans(n_clusters=3, random_state=42)
        df["Segment"] = kmeans.fit_predict(X_scaled)

        # Show segment distribution
        segment_counts = df["Segment"].value_counts()
        st.bar_chart(segment_counts)

        # Save model
        joblib.dump(kmeans, "customer_segmentation.pkl")

    # ✅ **Step 4: Consumer Behavior Trends**
    st.subheader("📈 Consumer Behavior Trends")
    if "purchase_frequency" in df.columns:
        st.line_chart(df.groupby("age")["purchase_frequency"].mean())

    st.success("✅ Customer Insights Analysis Complete!")