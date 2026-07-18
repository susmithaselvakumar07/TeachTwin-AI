import streamlit as st
import database.database
# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="centered"
)

# -------------------------
# Main Logo
# -------------------------
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.image("logo.jpeg", width=300)

st.write("")
st.write("")
st.write("")

# -------------------------
# Get Started Button
# -------------------------
if st.button("🚀 Enter TeachTwin AI", use_container_width=True):
    st.switch_page("pages/1_📖_Introduction.py")
