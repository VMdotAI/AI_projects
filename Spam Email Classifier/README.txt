README FILE WITH STEP-BY-STEP EXPLANATION

🚀 Spam Email Classifier using Google Colab (100% Free)
Building the Spam Email Classifier using Google Colab, which provides free GPU/TPU compute and is completely cloud-based.

📌 Step 1: Open Google Colab & Set Up Environment
Go to Google Colab.
Click "New Notebook".
Enable GPU (optional for deep learning models):
Go to Runtime → Change runtime type → Select GPU

📌 Step 2: Install Required Libraries
Google Colab already has most of these installed, but just in case:

//python

!pip install pandas numpy scikit-learn nltk

📌 Step 3: Load the Dataset
We'll use the SpamAssassin dataset, which contains labeled spam and non-spam emails.

//Download dataset:
//python

!wget https://spamassassin.apache.org/old/publiccorpus/20030228_spam.tar.bz2
!wget https://spamassassin.apache.org/old/publiccorpus/20030228_easy_ham.tar.bz2

//Extract dataset:
//python

import tarfile

def extract_tar(file_name):
    with tarfile.open(file_name, "r:bz2") as tar:
        tar.extractall()

extract_tar("20030228_spam.tar.bz2")
extract_tar("20030228_easy_ham.tar.bz2")

📌 Step 4: Preprocess the Data
We'll convert emails into numerical features using TF-IDF Vectorization.

//python

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import nltk
import re

nltk.download('stopwords')
from nltk.corpus import stopwords

# Load spam and ham emails
spam_dir = "spam"
ham_dir = "easy_ham"

def load_emails(directory, label):
    emails = []
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r", encoding="latin-1") as f:
            emails.append((f.read(), label))
    return emails

spam_emails = load_emails(spam_dir, 1)
ham_emails = load_emails(ham_dir, 0)

# Create DataFrame
df = pd.DataFrame(spam_emails + ham_emails, columns=["text", "label"])

# Preprocess text
def clean_text(text):
    text = re.sub(r'\W+', ' ', text)  # Remove special characters
    text = text.lower()  # Convert to lowercase
    text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])  # Remove stopwords
    return text

df["text"] = df["text"].apply(clean_text)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.2, random_state=42)

# Convert text to numerical features
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

📌 Step 5: Train the Spam Classifier
We'll use Naïve Bayes, a popular algorithm for text classification.

//python

# Train model
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Make predictions
y_pred = model.predict(X_test_tfidf)

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

📌 Step 6: Test with Custom Email Input
You can now test your classifier with any email text!

//python

def predict_spam(email_text):
    email_tfidf = vectorizer.transform([email_text])
    prediction = model.predict(email_tfidf)[0]
    return "Spam" if prediction == 1 else "Not Spam"

# Example
email = "Congratulations! You've won a free iPhone! Click here to claim."
print(predict_spam(email))

📌 Step 7: Save & Deploy Model (Optional)
If you want to deploy the model, save it first:

//python
import pickle

# Save model and vectorizer
pickle.dump(model, open("spam_classifier.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
