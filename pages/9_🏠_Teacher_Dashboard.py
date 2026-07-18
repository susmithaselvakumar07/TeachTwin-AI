import streamlit.components.v1 as components
from streamlit_javascript import st_javascript
import os
import sqlite3
from ai.pdf_reader import extract_pdf_text

import streamlit as st
from datetime import datetime
from database.qr_generator import generate_qr
# ------------------------------------
# Page Configuration
# ------------------------------------
st.set_page_config(
    page_title="TeachTwin AI",
    page_icon="favicon.png",
    layout="wide"
)
# -------------------------
# Login Check
# -------------------------
if not st.session_state.get("logged_in", False):
    st.switch_page("pages/6_🔐_Teacher_Login.py")


# ------------------------------------
# Hide Streamlit Menu & Footer
# ------------------------------------
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ------------------------------------
# Greeting Logic
# ------------------------------------
hour = datetime.now().hour

if hour < 12:
    greeting = "☀ Good Morning"
elif hour < 17:
    greeting = "🌤 Good Afternoon"
elif hour < 21:
    greeting = "🌇 Good Evening"
else:
    greeting = "🌙 Good Night"

teacher_name = st.session_state.get("teacher_name", "Teacher")

teacher_id = st.session_state.get("teacher_id", "Not Available")

# ------------------------------------
# Dashboard Statistics
# ------------------------------------
conn = sqlite3.connect("teachtwin.db")
cursor = conn.cursor()

# Total Students
cursor.execute("""
SELECT COUNT(*)
FROM student_teacher
WHERE teacher_id=?
""", (teacher_id,))
student_count = cursor.fetchone()[0]

# Total Materials
cursor.execute("""
SELECT COUNT(*)
FROM materials
WHERE teacher_id=?
""", (teacher_id,))
material_count = cursor.fetchone()[0]

# Total Assignments
cursor.execute("""
SELECT COUNT(*)
FROM assignments
WHERE teacher_id=?
""", (teacher_id,))
assignment_count = cursor.fetchone()[0]

# Total Submissions
cursor.execute("""
SELECT COUNT(*)
FROM submissions
WHERE assignment_id IN
(
SELECT id
FROM assignments
WHERE teacher_id=?
)
""", (teacher_id,))
submission_count = cursor.fetchone()[0]

conn.close()

# ------------------------------------
# Header
# ------------------------------------
col1, col2, col3 = st.columns([7,1,1])

with col1:
    st.title("🤖 TeachTwin AI")

with col2:
    st.image("favicon.png", width=55)

with col3:
    if st.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("app.py")

# ------------------------------------
# Welcome Card
# ------------------------------------
st.markdown(f"""
<div style="
background:linear-gradient(90deg,#2563EB,#4F46E5);
padding:25px;
border-radius:20px;
color:white;
margin-bottom:20px;
">

<h2>{greeting}, {teacher_name} 👋</h2>

<p style="font-size:18px;">
Welcome back to <b>TeachTwin AI</b>.<br>
Your AI Twin is ready to teach your students.
</p>

</div>
""", unsafe_allow_html=True)

# ------------------------------------
# Statistics Cards
# ------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "👨‍🎓 Students",
        student_count
    )

with c2:
    st.metric(
        "📚 Materials",
        material_count
    )

with c3:
    st.metric(
        "📝 Assignments",
        assignment_count
    )

with c4:
    st.metric(
        "📥 Submissions",
        submission_count
    )

# ------------------------------------
# TeachTwin ID Card
# ------------------------------------
st.markdown(f"""
<div style="
background:white;
padding:25px;
border-radius:18px;
box-shadow:0px 4px 12px rgba(0,0,0,0.12);
margin-bottom:20px;
">

<h4 style="color:#2563EB;">
🆔 Your TeachTwin ID
</h4>

<h2 style="
text-align:center;
color:#1E293B;
">
{teacher_id}
</h2>

<p style="
text-align:center;
color:gray;
">
Share this ID with your students to connect with your AI Twin.
</p>

</div>
""", unsafe_allow_html=True)

# ------------------------------------
# Buttons
# ------------------------------------
btn1, btn2 = st.columns(2)

with btn1:

    if st.button("📋 Copy ID", use_container_width=True):

        st_javascript(
            f"navigator.clipboard.writeText('{teacher_id}')"
        )

        st.success("✅ TeachTwin ID copied to clipboard!")
with btn2:

    if st.button("📱 Generate QR", use_container_width=True):

        qr_path = generate_qr(teacher_id)

        st.success("QR Generated Successfully!")

        st.image(qr_path, width=250)

        with open(qr_path, "rb") as file:

            st.download_button(
                "⬇ Download QR",
                file,
                file_name=f"{teacher_id}.png",
                mime="image/png",
                use_container_width=True
            )    
st.divider()

# ------------------------------------
# Quick Actions
# ------------------------------------

st.divider()

st.subheader("⚡ Quick Actions")

col1, col2 = st.columns(2)

# -----------------------
# Left Column
# -----------------------
with col1:

    if st.button("📝 Create Assignment", use_container_width=True):
        st.switch_page("pages/14_📝_Create_Assignment.py")

    if st.button("📚 Upload Study Material", use_container_width=True):
        st.success("Scroll down to upload your PDF.")

# -----------------------
# Right Column
# -----------------------
with col2:

    if st.button("📥 View Student Submissions", use_container_width=True):
        st.switch_page("pages/16_📥_View_Submissions.py")

    if st.button("🤖 AI Assistant", use_container_width=True):
        st.info("Coming Soon 🚀")


# ------------------------------------
# Upload Study Material
# ------------------------------------
st.subheader("📚 Upload Study Material")

uploaded_file = st.file_uploader(
    "Choose PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    # Create folder if it doesn't exist
    os.makedirs("uploads/materials", exist_ok=True)

    file_path = os.path.join(
        "uploads/materials",
        uploaded_file.name
    )

    # Save uploaded PDF
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read PDF
    extracted_text = extract_pdf_text(file_path)

    # Save into database
    conn = sqlite3.connect("teachtwin.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO materials
    (teacher_id, file_name, extracted_text)
    VALUES (?, ?, ?)
    """, (
        teacher_id,
        uploaded_file.name,
        extracted_text
    ))

    conn.commit()
    conn.close()

    st.success("✅ PDF Uploaded Successfully!")

    st.text_area(
        "Extracted Text",
        extracted_text,
        height=250
    )
# ------------------------------------
# Uploaded Materials
# ------------------------------------

st.divider()

st.subheader("📚 Uploaded Study Materials")

conn = sqlite3.connect("teachtwin.db")
cursor = conn.cursor()

cursor.execute("""
SELECT id, file_name
FROM materials
WHERE teacher_id=?
ORDER BY id DESC
""", (teacher_id,))

materials = cursor.fetchall()


if len(materials) == 0:

    st.info("No study materials uploaded yet.")

else:

    for material in materials:

        col1, col2 = st.columns([8,1])

        with col1:
            st.write(f"📄 {material[1]}")

        with col2:

            if st.button("🗑", key=f"delete_{material[0]}"):

                conn = sqlite3.connect("teachtwin.db")
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
