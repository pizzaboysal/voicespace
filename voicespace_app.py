import streamlit as st
from firebase_config import db  # Firestore instance
from datetime import datetime

# page setup
st.set_page_config(page_title="VoiceSpace — Anonymous Feedback", layout="wide")

# session state
if "teacher_user" not in st.session_state:
    st.session_state.teacher_user = None  # Stores logged-in teacher info

# styles
st.markdown("""
<style>
body { font-family: 'Roboto', sans-serif; 
       background-image: url('https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1350&q=80'); 
       background-size: cover; background-attachment: fixed; color: #ECF0F1; }
.stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div>select { 
       background-color: #34495E; color: white; border-radius: 5px; padding: 5px; }
.stButton>button { background-color: #1ABC9C; color: white; border-radius: 5px; padding: 0.5em 1em; font-weight: bold; }

.top-right {
    position: fixed;
    top: 10px;
    right: 20px;
    background-color: rgba(26, 188, 156, 0.8);
    padding: 5px 10px;
    border-radius: 5px;
    color: white;
    font-weight: bold;
    z-index: 100;
}
</style>
""", unsafe_allow_html=True)

# Display logged in teacher
if st.session_state.teacher_user:
    st.markdown(f'<div class="top-right">Logged in as: {st.session_state.teacher_user["email"]}</div>', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("VoiceSpace")

# CSS for nicer buttons
st.markdown("""
<style>
/* Sidebar container buttons (radio buttons, etc.) */
[data-testid="stSidebar"] div[role="radiogroup"] label {
    background-color: #1F3B5A;  /* Darker blue */
    color: white;
    border-radius: 10px;
    padding: 0.7em 1em;
    margin-bottom: 5px;
    display: block;
    font-weight: bold;
    font-size: 1em;
    cursor: pointer;
}

/* Sidebar hover effect */
[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background-color: #16293B;  /* Even darker blue on hover */
}

/* Other buttons on the page remain unchanged */
.stButton>button {
    background-color: #1ABC9C;
    color: white;
    border-radius: 10px;
    padding: 0.7em 1.5em;
    font-weight: bold;
    font-size: 1.1em;
}
</style>
""", unsafe_allow_html=True)


# Initialize current page
if "page" not in st.session_state:
    st.session_state.page = "Submit Feedback"

# Sidebar buttons
if st.sidebar.button("Submit Feedback"):
    st.session_state.page = "Submit Feedback"
if st.sidebar.button("Teacher/Administrator Dashboard"):
    st.session_state.page = "Teacher/Administrator Dashboard"
if st.sidebar.button("Help Centers"):
    st.session_state.page = "Help Centers"

page = st.session_state.page



# Header
st.markdown("""
<div style="background-color: rgba(44, 62, 80, 0.9); padding:30px; border-radius:10px;">
    <h1>VoiceSpace</h1>
    <h3>Anonymous Feedback for Students</h3>
    <p>Empowering students to safely report discriminatory behavior or inequitable practices.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Student Feedback Page
if page == "Submit Feedback":
    st.image("https://img.icons8.com/ios/50/1ABC9C/edit.png", width=50)
    st.subheader("Submit Anonymous Feedback")
    st.write("Your identity will **not** be recorded.")

    teachers = db.collection("teachers").stream()
    teacher_options = {t.id: t.to_dict().get('name', 'Unknown') for t in teachers}

    if teacher_options:
        selected_teacher_id = st.selectbox(
            "Select Teacher", options=list(teacher_options.keys()),
            format_func=lambda x: teacher_options[x]
        )
        category_options = ["Discrimination", "Microaggression", "Unfair Grading", "Other"]
        category = st.selectbox("Category", category_options)
        message = st.text_area("Describe what happened:", height=200)

        if st.button("Submit Message"):
            if not message.strip():
                st.warning("Please write a message before submitting.")
            else:
                db.collection("anonymous_messages").document().set({
                    "teacher_id": selected_teacher_id,
                    "category": category,
                    "message": message,
                    "created_at": datetime.utcnow()
                })
                st.success("Your feedback has been submitted anonymously.")
    else:
        st.warning("No teachers available yet. Ask your teacher to create an account first.")

# Teacher Dashboard Page
elif page == "Teacher/Administrator Dashboard":
    st.image("https://img.icons8.com/ios/50/1ABC9C/teacher.png", width=50)
    st.subheader("Teacher/Administrator Dashboard")

    if not st.session_state.teacher_user:
        st.write("Please log in or sign up to view your messages.")

        action = st.radio("Choose Action", ["Signup", "Login"])
        email = st.text_input("Email", key="email")
        password = st.text_input("Password", type="password", key="password")

        if st.button("Submit"):
            if not email or not password:
                st.warning("Please enter both email and password.")
            else:
                if action == "Signup":
                    # Check if email already exists
                    existing = db.collection("teachers").where("email", "==", email).stream()
                    if any(existing):
                        st.warning("Email already exists. Please login.")
                    else:
                        user_doc = db.collection("teachers").document()
                        user_doc.set({
                            "email": email,
                            "password": password,  # Plaintext for simplicity
                            "uid": user_doc.id,
                            "created_at": datetime.utcnow()
                        })
                        st.success("Account created! You are now logged in.")
                        st.session_state.teacher_user = {"email": email, "id": user_doc.id}
                elif action == "Login":
                    # Find matching teacher
                    teachers_query = db.collection("teachers").where("email", "==", email).where("password", "==", password).stream()
                    teacher_list = list(teachers_query)
                    if teacher_list:
                        st.success("Logged in successfully.")
                        teacher_doc = teacher_list[0]
                        st.session_state.teacher_user = {"email": email, "id": teacher_doc.id}
                    else:
                        st.error("Invalid email or password.")

    # Display messages if logged in
    if st.session_state.teacher_user:
        st.subheader("Messages Sent to You")
        teacher_uid = st.session_state.teacher_user["id"]
        messages = db.collection("anonymous_messages").where("teacher_id", "==", teacher_uid).stream()
        found = False
        for msg in messages:
            found = True
            data = msg.to_dict()
            st.markdown(f"**Category:** {data['category']}")
            st.markdown(f"**Message:** {data['message']}")
            st.markdown(f"Submitted: {data['created_at']}")
            st.markdown("---")
        if not found:
            st.info("No messages yet.")

# Help Center
elif page == "Help Centers":
    st.image("https://img.icons8.com/ios/50/1ABC9C/help.png", width=50)
    st.subheader("Help Centers")
    st.markdown("""
    <div style="background-color:#16A085; color:white; padding:20px; border-radius:10px;">
    - **Counseling Services:** <a href='https://www.mentalhealth.gov/get-help' target='_blank' style='color:white;'>Visit Website</a><br>
    - **Equity & Inclusion Office:** <a href='https://www.ed.gov/equity' target='_blank' style='color:white;'>Learn More</a><br>
    - **Peer Support Groups:** Contact your school's student wellness office.<br>
    - **National Sexual Assault Hotline:** <a href='https://www.rainn.org/' target='_blank' style='color:white;'>1-800-656-HOPE (4673)</a><br>
    - **Crisis Text Line:** Text **HOME** to 741741 for confidential support.
    </div>
    """, unsafe_allow_html=True)
