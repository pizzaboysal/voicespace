import streamlit as st
from firebase_config import db  # Firestore instance
import pyrebase
from datetime import datetime

# --- Firebase Auth configuration for teachers ---
firebaseConfig = {
    "apiKey": "AIzaSyB5xENCIYsX8JD00KK8Iaa0V1Qvh8zVV0E",
    "authDomain": "voicespace-ee2a5.firebaseapp.com",
    "databaseURL": "https://voicespace-ee2a5-default-rtdb.firebaseio.com/",
    "projectId": "voicespace-ee2a5",
    "storageBucket": "voicespace-ee2a5.firebasestorage.app",
    "messagingSenderId": "84971515256",
    "appId": "1:84971515256:web:5e9210f252aa90747e2c8d",
    "measurementId": "G-Q6SDMVD6GW"
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# --- App setup ---
st.set_page_config(page_title="VoiceSpace — Anonymous Feedback for Students", layout="wide")

# --- Custom CSS for fonts, background, and links ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
body { font-family: 'Roboto', sans-serif; background-image: url('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1350&q=80'); background-size: cover; background-attachment: fixed; color: #ECF0F1; }
.sidebar .sidebar-content { background-color: rgba(52, 73, 94, 0.9); padding: 20px; border-radius: 10px; }
h1, h3 { color: #ECF0F1; }
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div>select { background-color: #34495E; color: white; border-radius: 5px; padding: 5px; }
.stButton>button { background-color: #1ABC9C; color: white; border-radius: 5px; padding: 0.5em 1em; font-weight: bold; }
.sidebar a { text-decoration: none !important; color: #1ABC9C !important; font-weight: 500; }
.sidebar a:hover { color: #16A085 !important; }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div style="background-color: rgba(44, 62, 80, 0.9); padding:30px; border-radius:10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.3);">
    <h1>🎙️ VoiceSpace</h1>
    <h3>Anonymous Feedback for Students</h3>
    <p>Empowering students to safely report discriminatory behavior, microaggressions, or inequitable practices.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- Sidebar navigation ---
st.sidebar.markdown("""
<div style="padding:10px">
<h3>Navigation</h3>
<p><a href="#student-feedback">📝 Submit Feedback</a></p>
<p><a href="#teacher-dashboard">👩‍🏫 Teacher Dashboard</a></p>
<p><a href="#help-centers">🤝 Help Centers</a></p>
</div>
""", unsafe_allow_html=True)

# --- Student Anonymous Feedback ---
st.markdown('<a name="student-feedback"></a>', unsafe_allow_html=True)
st.header("📝 Submit Anonymous Feedback")
st.write("Your identity will **not** be recorded.")

# Fetch teachers for dropdown
teachers = db.collection("teachers").stream()
teacher_options = {t.id: t.to_dict()['name'] for t in teachers}

selected_teacher_id = st.selectbox("Select Teacher", options=list(teacher_options.keys()),
                                   format_func=lambda x: teacher_options[x])

category_options = ["Discrimination", "Microaggression", "Unfair Grading", "Other"]
category = st.selectbox("Category", category_options)
message = st.text_area("Describe what happened:", height=200)

if st.button("Submit Message", key="submit_feedback"):
    if not message.strip():
        st.warning("⚠️ Please write a message before submitting.")
    else:
        db.collection("anonymous_messages").document().set({
            "teacher_id": selected_teacher_id,
            "category": category,
            "message": message,
            "created_at": datetime.utcnow()
        })
        st.success("✅ Your feedback has been submitted anonymously. Thank you for speaking up!")

# --- Teacher Login & Dashboard ---
st.markdown('<a name="teacher-dashboard"></a>', unsafe_allow_html=True)
st.header("👩‍🏫 Teacher Login & Dashboard")

login_choice = st.radio("Choose Action", ["Login", "Signup"])

teacher_email = st.text_input("Email", key="teacher_email")
teacher_password = st.text_input("Password", type="password", key="teacher_password")

if login_choice == "Signup" and st.button("Create Account"):
    try:
        user = auth.create_user_with_email_and_password(teacher_email, teacher_password)
        st.success("Account created! You can now login.")
        # Add to Firestore teachers collection
        db.collection("teachers").document(user['localId']).set({
            "name": teacher_email.split("@")[0],  # Default name
            "email": teacher_email,
            "uid": user['localId'],
            "created_at": datetime.utcnow()
        })
    except Exception as e:
        st.error(f"Error: {e}")

if login_choice == "Login" and st.button("Login"):
    try:
        user = auth.sign_in_with_email_and_password(teacher_email, teacher_password)
        st.success("Logged in successfully!")
        teacher_uid = user['localId']

        # Fetch messages for this teacher
        st.subheader("📨 Messages Sent to You")
        messages = db.collection("anonymous_messages").where("teacher_id", "==", teacher_uid).stream()
        for msg in messages:
            data = msg.to_dict()
            st.markdown(f"**Category:** {data['category']}")
            st.markdown(f"**Message:** {data['message']}")
            st.markdown("---")
    except Exception as e:
        st.error(f"Login failed: {e}")

# --- Help Centers Section ---
st.markdown('<a name="help-centers"></a>', unsafe_allow_html=True)
st.subheader("🤝 Places You Can Get Help")
st.markdown("""
<div style="background-color:#16A085; color:white; padding:20px; border-radius:10px; box-shadow: 1px 1px 8px rgba(0,0,0,0.3);">
- **Counseling Services:** <a href='https://www.mentalhealth.gov/get-help' target='_blank' style='color:white;'>Visit Website</a><br>
- **Equity & Inclusion Office:** <a href='https://www.ed.gov/equity' target='_blank' style='color:white;'>Learn More</a><br>
- **Peer Support Groups:** Contact your school's student wellness office.<br>
- **National Sexual Assault Hotline:** <a href='https://www.rainn.org/' target='_blank' style='color:white;'>1-800-656-HOPE (4673)</a><br>
- **Crisis Text Line:** Text **HOME** to 741741 for confidential support.
</div>
""", unsafe_allow_html=True)
