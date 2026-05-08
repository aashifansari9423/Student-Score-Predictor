import streamlit as st
import joblib
import pandas as pd
import numpy as np
import hashlib
import json
import os

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =====================================
# USER DATABASE FILE
# =====================================
USER_DB_FILE = "users.json"

def load_users():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =====================================
# SESSION STATE
# =====================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "login"

# =====================================
# GLOBAL CSS - FORCE WHITE TEXT ON ALL DEVICES
# =====================================
global_css = """
<style>
    /* Force EVERYTHING white */
    .stApp, .stApp * {
        color: #ffffff !important;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    /* Force all input text to be white */
    input, textarea, select, .stTextInput input, .stNumberInput input {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        background-color: #1a1a2e !important;
    }
    
    /* Placeholder color */
    input::placeholder, .stTextInput input::placeholder {
        color: #888888 !important;
        -webkit-text-fill-color: #888888 !important;
    }
    
    /* Number input specific */
    .stNumberInput input {
        background-color: #1a1a2e !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    
    /* Select box input */
    div[data-baseweb="select"] input {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    
    /* Labels */
    .stNumberInput label, .stSelectbox label {
        color: #cbd5e0 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: #00adb5 !important;
        color: white !important;
        border: none !important;
    }
    
    .stButton > button:hover {
        background: #007a7f !important;
    }
    
    /* Result card */
    .result-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 2px solid #00adb5;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        margin: 1.5rem 0;
    }
    
    .result-label {
        color: #888888 !important;
    }
    
    .result-score {
        color: #00adb5 !important;
        font-size: 3rem;
        font-weight: 800;
    }
    
    .result-score span {
        color: #666666 !important;
    }
    
    /* Success/Info/Warning */
    .stSuccess {
        background-color: rgba(0, 173, 181, 0.2) !important;
        color: #ffffff !important;
    }
    
    .stInfo {
        background-color: rgba(59, 130, 246, 0.2) !important;
        color: #ffffff !important;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.2) !important;
        color: #ffffff !important;
    }
    
    /* Auth container */
    .auth-container {
        background: rgba(18, 18, 30, 0.95);
        border-radius: 20px;
        padding: 2rem;
        max-width: 420px;
        margin: 60px auto;
        border: 1px solid #334155;
        text-align: center;
    }
    
    .auth-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
    }
    
    hr {
        margin: 1.2rem 0;
        border: none;
        height: 1px;
        background: #334155;
    }
    
    .footer-text {
        margin-top: 1.2rem;
        color: #666 !important;
        font-size: 0.7rem;
    }
    
    /* Divider */
    div[data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Mobile specific */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        h1 {
            font-size: 1.4rem !important;
        }
        .result-score {
            font-size: 2rem;
        }
        input, .stTextInput input, .stNumberInput input {
            font-size: 16px !important;
            padding: 0.6rem !important;
        }
    }
</style>
"""

# =====================================
# AUTH PAGE
# =====================================
def show_auth_page():
    st.markdown(global_css, unsafe_allow_html=True)
    
    users = load_users()
    
    st.markdown("""
    <div class="auth-container">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎓</div>
        <div class="auth-title">Student Score Predictor</div>
    """, unsafe_allow_html=True)
    
    if st.session_state.auth_mode == "login":
        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        if st.button("Sign In", use_container_width=True):
            if username and password:
                if username in users and users[username]["password"] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter username and password")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("Create New Account", use_container_width=True, key="switch_to_signup"):
            st.session_state.auth_mode = "signup"
            st.rerun()
    
    else:
        username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
        password = st.text_input("Password", type="password", placeholder="Choose a password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="signup_confirm")
        
        if st.button("Sign Up", use_container_width=True):
            if not username or not password:
                st.warning("Please fill all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 4:
                st.warning("Password must be at least 4 characters")
            elif username in users:
                st.error("Username already exists")
            else:
                users[username] = {
                    "password": hash_password(password)
                }
                save_users(users)
                st.success("Account created successfully!")
                st.session_state.auth_mode = "login"
                st.rerun()
        
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("Back to Sign In", use_container_width=True, key="switch_to_login"):
            st.session_state.auth_mode = "login"
            st.rerun()
    
    st.markdown('<div class="footer-text">Secure • Free • No email required</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# LOAD MODEL
# =====================================
@st.cache_resource
def load_models():
    model = joblib.load("student_model.pkl")
    columns = joblib.load("model_columns.pkl")
    return model, columns

# =====================================
# MAIN APP
# =====================================
def show_main_app():
    st.markdown(global_css, unsafe_allow_html=True)
    
    # Top bar
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<div style="background: rgba(0,173,181,0.1); padding: 0.4rem 1rem; border-radius: 50px; display: inline-block;">Welcome, {st.session_state.username}</div>', unsafe_allow_html=True)
    with col2:
        if st.button("Sign Out", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()
    
    st.markdown("<h1 style='text-align: center;'>Student Score Predictor</h1>", unsafe_allow_html=True)
    
    # Load model
    model, columns = load_models()
    
    # Input fields
    col1, col2 = st.columns(2)
    
    with col1:
        hours = st.number_input("Hours Studied", min_value=0.0, max_value=24.0, value=5.0, step=0.5)
        attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=75.0, step=5.0)
        previous = st.number_input("Previous Score", min_value=0.0, max_value=100.0, value=60.0, step=5.0)
        sleep = st.number_input("Sleep Hours", min_value=0.0, max_value=12.0, value=7.0, step=0.5)
        motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
        teacher = st.selectbox("Teacher Quality", ["Poor", "Average", "Good"])
        school = st.selectbox("School Type", ["Public", "Private"])
    
    with col2:
        internet = st.selectbox("Internet Access", ["Yes", "No"])
        income = st.selectbox("Family Income", ["Low", "Medium", "High"])
        parent = st.selectbox("Parental Involvement", ["Low", "Medium", "High"])
        education = st.selectbox("Parent Education", ["School", "College"])
        peer = st.selectbox("Peer Influence", ["Negative", "Neutral", "Positive"])
        resources = st.selectbox("Learning Resources", ["Low", "Medium", "High"])
        activities = st.selectbox("Extracurricular Activities", ["Yes", "No"])
    
    # Predict button
    if st.button("Predict Score", use_container_width=True):
        
        data = {
            "Hours_Studied": hours,
            "Attendance": attendance,
            "Previous_Scores": previous,
            "Sleep_Hours": sleep,
            "Motivation_Level": motivation,
            "Teacher_Quality": teacher,
            "School_Type": school,
            "Internet_Access": internet,
            "Family_Income": income,
            "Parental_Involvement": parent,
            "Parental_Education_Level": education,
            "Peer_Influence": peer,
            "Learning_Resources": resources,
            "Extracurricular_Activities": activities
        }
        
        input_df = pd.DataFrame([data])
        input_df = pd.get_dummies(input_df)
        input_df = input_df.reindex(columns=columns, fill_value=0)
        
        prediction = model.predict(input_df)
        final_score = max(40, min(100, prediction[0]))
        final_score = int(round(final_score))
        
        # Result
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">PREDICTED EXAM SCORE</div>
            <div class="result-score">{final_score}<span> / 100</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Performance message
        if final_score >= 85:
            st.success("Exceptional Performance")
            st.balloons()
        elif final_score >= 70:
            st.success("Good Performance")
        elif final_score >= 55:
            st.info("Satisfactory Performance")
        else:
            st.warning("Needs Improvement")
        
        # Recommendations
        recommendations = []
        if hours < 6:
            recommendations.append("Increase study hours to 6-8 hours daily")
        if attendance < 75:
            recommendations.append("Improve attendance to 80% or higher")
        if sleep < 7:
            recommendations.append("Get 7-9 hours of sleep for better focus")
        if motivation == "Low":
            recommendations.append("Set daily goals to boost motivation")
        if teacher == "Poor":
            recommendations.append("Seek additional tutoring or online resources")
        if resources == "Low":
            recommendations.append("Utilize free online learning materials")
        if peer == "Negative":
            recommendations.append("Join positive study groups")
        
        if recommendations:
            st.markdown("### Recommendations")
            for rec in recommendations:
                st.info(rec)
        else:
            st.success("Excellent study habits. Maintain your routine")
    
    # Footer
    st.markdown("---")
    st.caption("Student Score Predictor | Powered by Machine Learning")

# =====================================
# MAIN ROUTER
# =====================================
if st.session_state.logged_in:
    show_main_app()
else:
    show_auth_page()
