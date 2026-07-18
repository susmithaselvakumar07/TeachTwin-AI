import streamlit as st

st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="wide"
)

# Top-right logo
left, right = st.columns([9, 1])

with right:
    st.image("favicon.png", width=55)

st.markdown(
    "<h1 style='text-align:center;'>✨ Choose Your Role</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 style='text-align:center; color:gray;'>Who are you?</h4>",
    unsafe_allow_html=True
)

st.write("")
st.write("")

col1, col2 = st.columns(2)

with col1:
    st.markdown("## 👨‍🏫 Teacher")
    st.write("Create your own AI Twin")
    st.write("Teach students anytime")
    st.write("Upload your knowledge")

    if st.button("Select Teacher", use_container_width=True):
        st.switch_page("pages/3_👨‍🏫_Teacher_Auth.py")

with col2:
    st.markdown("## 🎓 Student")
    st.write("Learn from your teacher's AI")
    st.write("Ask unlimited questions")
    st.write("Study anytime")

    if st.button("Select Student", use_container_width=True):
        st.switch_page("pages/4_🎓_Student_Auth.py")
