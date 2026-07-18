import streamlit as st

st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="centered"
)

# -------------------------
# Top Right Logo
# -------------------------
left, right = st.columns([9, 1])

with right:
    st.image("favicon.png", width=55)

st.markdown(
    "<h1 style='text-align:center;'>👨‍🏫 Welcome, Teacher</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center; color:gray;'>Create your AI Twin and inspire students beyond the classroom.</h4>",
    unsafe_allow_html=True
)

st.write("")
st.write("")

col1, col2 = st.columns(2)

with col1:
    if st.button("✨ Create Account", use_container_width=True):
        st.switch_page("pages/5_📝_Teacher_SignUp.py")

with col2:
    if st.button("🔑 Sign In", use_container_width=True):
        st.switch_page("pages/6_🔐_Teacher_Login.py")
