import streamlit as st
import time

st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="wide"
)

# -----------------------------
# Top Right Logo
# -----------------------------
col1, col2 = st.columns([8,1])

with col2:
    st.image("favicon.png", width=70)

st.markdown(
"""
<h1 style='text-align:center; color:#1E88E5;'>
👋 Welcome to the Future of Learning
</h1>
""",
unsafe_allow_html=True)

st.divider()

messages = [
    "🧠 Learn exactly the way your teacher teaches.",
    "📚 Upload Notes, PDFs & PPTs.",
    "🤖 AI learns your teacher's teaching style.",
    "💬 Ask questions anytime. Learn anytime."
]

placeholder = st.empty()

for msg in messages:
    placeholder.info(msg)
    time.sleep(1)

st.divider()

st.subheader("⭐ Why TeachTwin AI?")

st.success("✔ Personalized for Every Teacher")

st.success("✔ Answers from Teacher's Own Materials")

st.success("✔ Available 24×7")

st.success("✔ Saves Time for Teachers & Students")

st.write("")

if st.button("🚀 Continue", use_container_width=True):
    st.switch_page("pages/2_👤_Role_Selection.py")
