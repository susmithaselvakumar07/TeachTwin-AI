import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv


# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    api_key = st.secrets.get("GOOGLE_API_KEY")


# -----------------------------
# Configure Gemini
# -----------------------------
if not api_key:
    st.error("Google API key not found.")
    st.stop()

genai.configure(api_key=api_key)


# -----------------------------
# Gemini Model
# -----------------------------
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# -----------------------------
# Ask TeachTwin AI
# -----------------------------
def ask_teachtwin(context, question):

    prompt = f"""
You are TeachTwin AI.

Answer the student's question using ONLY the teacher's uploaded study material.

Teacher's Study Material:
{context}

Student Question:
{question}

If the answer cannot be found in the study material, say:

Sorry, this topic is not available in your teacher's uploaded notes.
"""

    try:

        response = model.generate_content(
            prompt
        )

        if response and response.text:

            return response.text

        return "Sorry, I could not generate an answer."

    except Exception as e:

        return f"AI Error: {str(e)}"
