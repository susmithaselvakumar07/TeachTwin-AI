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
# Professional Header
# ------------------------------------

header_col1, header_col2 = st.columns([8, 2])

with header_col1:
    st.markdown(
        """
        <h1 style="margin-bottom:0;">
            🤖 TeachTwin AI
        </h1>
        <p style="color:gray; margin-top:0;">
            Your Knowledge. Your AI. Your Students.
        </p>
        """,
        unsafe_allow_html=True
    )

with header_col2:

    st.image("favicon.png", width=55)

    if st.button("🚪 Logout", use_container_width=True):
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
# TeachTwin Connection Center
# ------------------------------------

st.divider()

st.subheader("🔗 Connect Students to Your AI Twin")

id_col, qr_col = st.columns([1.5, 1])

with id_col:

    st.info(
        f"""
🆔 Your TeachTwin ID

{teacher_id}

Share this ID with your students to connect them with your AI Twin.
"""
    )

    components.html(
        f"""
        <button onclick="copyID()"
        style="
        width:100%;
        padding:12px;
        border-radius:10px;
        border:none;
        background:#2563EB;
        color:white;
        font-size:16px;
        cursor:pointer;
        ">
        📋 Copy TeachTwin ID
        </button>

        <script>
        function copyID() {{
            navigator.clipboard.writeText("{teacher_id}");
            alert("TeachTwin ID copied successfully!");
        }}
        </script>
        """,
        height=60
    )

with qr_col:

    st.info(
        """
📱 Student Connection

Generate a QR code for quick student connection.
"""
    )

    if st.button(
        "📱 Generate QR Code",
        use_container_width=True,
        key="generate_teacher_qr"
    ):

        qr_path = generate_qr(teacher_id)

        st.success("QR Code Generated Successfully!")

        st.image(qr_path, width=220)

        with open(qr_path, "rb") as file:

            st.download_button(
                "⬇ Download QR Code",
                file,
                file_name=f"{teacher_id}.png",
                mime="image/png",
                use_container_width=True,
                key="download_teacher_qr"
            )



# ------------------------------------
# Quick Actions
# ------------------------------------

st.divider()

st.subheader("⚡ Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(
        "📝 Create Assignment",
        use_container_width=True,
        key="quick_create_assignment"
    ):
        st.switch_page("pages/14_📝_Create_Assignment.py")

with col2:
    if st.button(
        "📚 Upload Material",
        use_container_width=True,
        key="quick_upload_material"
    ):
        st.info("Scroll down to upload your study material.")

with col3:
    if st.button(
        "📥 Submissions",
        use_container_width=True,
        key="quick_submissions"
    ):
        st.switch_page("pages/16_📥_View_Submissions.py")

with col4:
    if st.button(
        "🤖 AI Assistant",
        use_container_width=True,
        key="quick_ai_assistant"
    ):
        st.info("AI Assistant coming soon 🚀")

# ------------------------------------
# Upload Study Material
# ------------------------------------

st.divider()

st.subheader("📤 Upload Study Material")

uploaded_file = st.file_uploader(
    "Choose a PDF study material",
    type=["pdf"],
    key="study_material_uploader"
)

if uploaded_file is not None:

    if st.button(
        "⬆️ Upload Study Material",
        use_container_width=True,
        key="upload_study_material"
    ):

        with st.spinner("Processing study material... 📚"):

            # Extract text from PDF
            extracted_text = extract_pdf_text(
                uploaded_file
            )

            # Save to database
            conn = sqlite3.connect(
                "teachtwin.db"
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO materials
                (teacher_id, file_name, extracted_text)
                VALUES (?, ?, ?)
                """,
                (
                    teacher_id,
                    uploaded_file.name,
                    extracted_text
                )
            )

            conn.commit()
            conn.close()

            st.success(
                "✅ Study material uploaded successfully!"
            )

            st.rerun()


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
conn.close()

if len(materials) == 0:

    st.info("No study materials uploaded yet.")

else:

    for material in materials:

        col1, col2 = st.columns([8, 1])

        with col1:
            st.write(f"📄 {material[1]}")

        with col2:

            if st.button("🗑", key=f"delete_{material[0]}"):

                delete_conn = sqlite3.connect("teachtwin.db")
                delete_cursor = delete_conn.cursor()

                delete_cursor.execute(
                    """
                    DELETE FROM materials
                    WHERE id = ? AND teacher_id = ?
                    """,
                    (material[0], teacher_id)
                )

                delete_conn.commit()
                delete_conn.close()

                st.success("Study material deleted successfully!")
                st.rerun()

        
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
