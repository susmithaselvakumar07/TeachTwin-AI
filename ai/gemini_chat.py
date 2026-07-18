import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load API Key
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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
'Sorry, this topic is not available in your teacher's uploaded notes.'
"""

    response = model.generate_content(prompt)

    return response.text
