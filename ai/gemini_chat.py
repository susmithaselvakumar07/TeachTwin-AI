import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load local .env
load_dotenv()

# Try local .env first
api_key = os.getenv("GOOGLE_API_KEY")

# If not available, use Streamlit Cloud Secrets
if not api_key:
    api_key = st.secrets.get("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")


def ask_teachtwin(context, question):

    prompt = f"""
You are TeachTwin AI.

Answer ONLY from the teacher's uploaded study material.

Study Material:
{context}

Student Question:
{question}

If the answer is not found in the study material, reply:
"Sorry, this topic is not available in your teacher's uploaded notes."
"""

    response = model.generate_content(prompt)

    return response.text
