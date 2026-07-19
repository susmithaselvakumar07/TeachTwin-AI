import streamlit as st
import sqlite3

from ai.gemini_chat import ask_teachtwin
from ai.search_notes import find_relevant_context


# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="wide"
)

st.title("🤖 TeachTwin AI")


# -----------------------------
# Login Check
# -----------------------------
student_email = st.session_state.get("student_email")

if not student_email:
    st.error("Please login first.")
    st.stop()


# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []


# -----------------------------
# Find Connected Teacher
# -----------------------------
conn = sqlite3.connect("teachtwin.db")
cursor = conn.cursor()

cursor.execute(
    """
    SELECT teacher_id
    FROM student_teacher
    WHERE student_email = ?
    """,
    (student_email,)
)

teacher = cursor.fetchone()

if teacher is None:
    conn.close()
    st.warning("You are not connected to any teacher.")
    st.stop()

teacher_id = teacher[0]


# -----------------------------
# Get Teacher Materials
# -----------------------------
cursor.execute(
    """
    SELECT extracted_text
    FROM materials
    WHERE teacher_id = ?
    """,
    (teacher_id,)
)

materials = cursor.fetchall()

conn.close()


if len(materials) == 0:
    st.warning(
        "Your teacher has not uploaded any study materials yet."
    )
    st.stop()


# -----------------------------
# Combine Study Materials
# -----------------------------
all_notes = []

for material in materials:
    all_notes.append(material[0])


# -----------------------------
# Display Chat History
# -----------------------------
for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message("user"):
            st.write(message["content"])

    elif message["role"] == "assistant":

        with st.chat_message("assistant"):
            st.write(message["content"])


# -----------------------------
# User Input
# -----------------------------
question = st.chat_input(
    "Ask TeachTwin anything..."
)


if question:

    # -----------------------------
    # Show User Message
    # -----------------------------
    with st.chat_message("user"):
        st.write(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # -----------------------------
    # AI Processing
    # -----------------------------
    with st.spinner("TeachTwin is thinking... 🤖"):

        st.write("🔍 Searching study material...")

        relevant_context = find_relevant_context(
            all_notes,
            question
        )

        st.write(
            "✅ Study material search completed."
        )


        if relevant_context.strip() == "":

            answer = (
                "Sorry, I couldn't find this topic "
                "in your teacher's uploaded notes."
            )

        else:

            st.write(
                "🤖 Sending question to Gemini..."
            )

            answer = ask_teachtwin(
                relevant_context,
                question
            )

            st.write(
                "✅ Gemini response received."
            )


    # -----------------------------
    # Show AI Message
    # -----------------------------
    with st.chat_message("assistant"):

        st.write(answer)


    # -----------------------------
    # Save AI Message
    # -----------------------------
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )