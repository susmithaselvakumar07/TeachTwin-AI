import streamlit as st

st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png"
)

st.title("🎓 Welcome Student")

tab1, tab2 = st.tabs(["Join TeachTwin", "Sign In"])

with tab1:
    st.subheader("Create Student Account")

    st.text_input("Full Name")
    st.text_input("Email")
    st.text_input("Password", type="password")
    st.text_input("College / School")
    st.text_input("Teacher Code")

    if st.button("Create Account"):
        st.success("Student account created successfully!")

with tab2:
    st.subheader("Student Sign In")

    st.text_input("Email", key="student_email")
    st.text_input("Password", type="password", key="student_password")

    if st.button("Sign In"):
        st.success("Login Successful!")
