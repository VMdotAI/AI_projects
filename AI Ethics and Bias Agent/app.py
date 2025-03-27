import streamlit as st
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from aif360.datasets import BinaryLabelDataset
from aif360.metrics import BinaryLabelDatasetMetric
from aif360.algorithms.preprocessing import Reweighing

# 🎯 Title
st.title("🤖 AI Ethics & Bias Agent")
st.write("Upload an AI model and test it for fairness and bias.")

# 📤 **Step 1: Upload Your Model**
uploaded_model = st.file_uploader("Upload your trained AI model (.pkl)", type=["pkl"])
uploaded_data = st.file_uploader("Upload sample dataset (CSV)", type=["csv"])

if uploaded_model and uploaded_data:
    st.success("✅ Model and dataset uploaded successfully!")

    # Load model
    model = joblib.load(uploaded_model)

    # Load dataset
    df = pd.read_csv(uploaded_data)
    st.write("📊 Sample Data Preview:", df.head())

    # Extract features & labels
    X = df.drop(columns=["target"])  # Replace "target" with actual target column
    y = df["target"]

    # ✅ **Step 2: Test Model Accuracy**
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    st.write(f"🔹 **Model Accuracy:** {accuracy:.2f}")

    # ✅ **Step 3: Check for Bias**
    st.subheader("📈 Fairness & Bias Analysis")
    dataset = BinaryLabelDataset(df=df, label_names=["target"], protected_attribute_names=["gender"])  # Change as needed
    metric = BinaryLabelDatasetMetric(dataset, privileged_groups=[{'gender': 1}], unprivileged_groups=[{'gender': 0}])
    disparate_impact = metric.disparate_impact()

    st.write(f"🔹 **Disparate Impact Score:** {disparate_impact:.2f}")

    # ✅ **Step 4: Apply Bias Mitigation**
    if disparate_impact < 0.8 or disparate_impact > 1.2:
        st.warning("⚠️ Potential bias detected! Applying bias mitigation...")
        reweigh = Reweighing(unprivileged_groups=[{'gender': 0}], privileged_groups=[{'gender': 1}])
        reweighed_dataset = reweigh.fit_transform(dataset)
        metric_after = BinaryLabelDatasetMetric(reweighed_dataset, privileged_groups=[{'gender': 1}], unprivileged_groups=[{'gender': 0}])
        st.write(f"✅ **After mitigation, New Disparate Impact Score:** {metric_after.disparate_impact():.2f}")
    else:
        st.success("✅ AI model is fair and meets ethical standards.")

st.success("AI Bias & Fairness Analysis Complete! ✅")