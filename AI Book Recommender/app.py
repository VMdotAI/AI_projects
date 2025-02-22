import streamlit as st
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import torch

# Load dataset
@st.cache_data
def load_data():
    books_df = pd.read_csv('goodbooks-10k.csv')
    books_df = books_df.dropna(subset=['title', 'genres', 'description'])
    books_df = books_df[['title', 'genres', 'author', 'description', 'average_rating']]
    return books_df

books_df = load_data()

# Load pre-trained model
@st.cache_resource
def load_model():
    return SentenceTransformer('paraphrase-MiniLM-L6-v2')

model = load_model()

# Convert book descriptions into vectors (Fix: Use `_model` instead of `model`)
@st.cache_resource
def compute_embeddings(_model, books_df):
    return _model.encode(books_df['description'].tolist(), convert_to_tensor=True)

book_embeddings = compute_embeddings(model, books_df)

# Function to get book recommendations
def get_recommendations(user_input, books_df, book_embeddings, model, top_n=5):
    query_embedding = model.encode([user_input], convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, book_embeddings)[0]
    top_results = torch.topk(similarities, k=top_n)

    results = []
    for score, book_idx in zip(top_results[0], top_results[1]):
        results.append(f"📖 {books_df.iloc[int(book_idx)]['title']} - ⭐ {books_df.iloc[int(book_idx)]['average_rating']} (Score: {score:.4f})")
    
    return results

# Streamlit UI
st.title("📚 AI-Based Book Recommendation System")
st.subheader("Find books similar to your favorites using AI!")

# User input
user_input = st.text_input("Enter a book title or describe your preferences:", "")

if user_input:
    st.write("🔍 Searching for similar books...")
    recommendations = get_recommendations(user_input, books_df, book_embeddings, model)
    
    st.write("### 📌 Recommended Books:")
    for book in recommendations:
        st.write(book)
