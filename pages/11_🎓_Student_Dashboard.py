import streamlit as st
import sqlite3

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="wide"
)

# -----------------------------
# Login Check
# -----------------------------
if "student_email" not in st.session_state:
    st.switch_page("pages/8_🔐_Student_Login.py")

student_name = st.session_state["student_name"]
student_email = st.session_state["student_email"]

# -----------------------------
# Get Dashboard Data
# -----------------------------
conn = sqlite3.connect("teachtwin.db")
cursor = conn.cursor()

cursor.execute("""
SELECT
teachers.full_name,
teachers.subject,
teachers.teachtwin_id
FROM student_teacher
JOIN teachers
ON student_teacher.teacher_id = teachers.teachtwin_id
WHERE student_teacher.student_email=?
""",(student_email,))

teacher = cursor.fetchone()

materials_count = 0
assignment_count = 0

if teacher:

    teacher_id = teacher[2]

    cursor.execute("""
    SELECT COUNT(*)
    FROM materials
    WHERE teacher_id=?
    """,(teacher_id,))
    materials_count = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM assignments
    WHERE teacher_id=?
    """,(teacher_id,))
    assignment_count = cursor.fetchone()[0]

conn.close()

# -----------------------------
# Header
# -----------------------------
left, middle, right = st.columns([7,1,1])

with left:
    st.title("🎓 TeachTwin AI")

with middle:
    st.image("favicon.png", width=55)

with right:

    if st.button("🚪 Logout"):

        st.session_state.clear()

        st.switch_page("app.py")

#-------------------------------
# Welcome Banner
#-------------------------------

st.markdown(f"""
<div style="
background:linear-gradient(90deg,#2563EB,#4F46E5);
padding:25px;
border-radius:20px;
color:white;
margin-bottom:20px;
">

<h2>👋 Welcome {student_name}</h2>

<p style="font-size:18px;">
Your AI learning assistant is ready to help you.
</p>

</div>
""",unsafe_allow_html=True)

st.divider()

# -----------------------------
# Connected Teacher
# -----------------------------
if teacher:

    st.markdown(f"""
<div style="
background:white;
padding:20px;
border-radius:18px;
box-shadow:0px 4px 10px rgba(0,0,0,0.12);
">

<h3>👨‍🏫 Connected Teacher</h3>

<b>Name :</b> {teacher[0]}<br>

<b>Subject :</b> {teacher[1]}<br>

<b>TeachTwin ID :</b> {teacher[2]}

</div>
""",unsafe_allow_html=True)

    st.markdown(f"""
### 👨‍🏫 {teacher[0]}

📚 **Subject:** {teacher[1]}

🆔 **TeachTwin ID:** {teacher[2]}
""")

else:

    st.warning("⚠️ You are not connected to any teacher.")

    if st.button("🤝 Join Teacher", use_container_width=True):
        st.switch_page("pages/10_🤝_Join_Teacher.py")

st.divider()

# -----------------------------
# Features
# -----------------------------
col1, col2, col3 = st.columns(3)

# -----------------------------
# AI Chat
# -----------------------------
with col1:

    if st.button("🤖 Chat with AI", use_container_width=True):

        if teacher:
            st.switch_page("pages/12_🤖_Student_AI_Chat.py")
        else:
            st.warning("Please connect with a teacher first.")
            st.switch_page("pages/10_🤝_Join_Teacher.py")

# -----------------------------
# Study Materials
# -----------------------------
with col2:

    if st.button("📚 Study Materials", use_container_width=True):

        if teacher:
            st.switch_page("pages/13_📄_Study_Materials.py")
        else:
            st.warning("Please connect with a teacher first.")
            st.switch_page("pages/10_🤝_Join_Teacher.py")

# -----------------------------
# Assignments
# -----------------------------
with col3:

    if st.button("📝 Assignments", use_container_width=True):

        if teacher:
            st.switch_page("pages/15_📝_Student_Assignments.py")
        else:
            st.warning("Please connect with a teacher first.")
            st.switch_page("pages/10_🤝_Join_Teacher.py")

st.divider()

# ------------------------------------
# Footer
# ------------------------------------

st.write("")
st.write("")

st.markdown("---")

st.markdown("""
<div style="
text-align:center;
padding:20px;
color:gray;
">

<h3>🤖 TeachTwin AI</h3>

<p><b>Your Knowledge. Your AI. Your Students.</b></p>

<p>Version 1.0</p>

</div>
""", unsafe_allow_html=True)
