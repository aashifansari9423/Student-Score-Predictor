import streamlit as st
import joblib
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

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

# =====================================
# SESSION STATE
# =====================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

# =====================================
# GOOGLE SIGN IN CSS
# =====================================
auth_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    .auth-container {
        background: rgba(18, 18, 30, 0.95);
        border-radius: 20px;
        padding: 2.5rem;
        max-width: 420px;
        margin: 80px auto;
        border: 1px solid #334155;
        text-align: center;
    }
    
    .auth-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    
    .auth-subtitle {
        color: #888888;
        font-size: 0.85rem;
        margin-bottom: 2rem;
    }
    
    .google-btn {
        background-color: #ffffff;
        color: #333333;
        border: none;
        border-radius: 50px;
        padding: 0.7rem 1.5rem;
        font-size: 0.9rem;
        font-weight: 500;
        width: 100%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        transition: all 0.3s ease;
    }
    
    .google-btn:hover {
        background-color: #f0f0f0;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.5rem 0;
        color: #666;
        font-size: 0.8rem;
    }
    
    .divider::before,
    .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #334155;
    }
    
    .divider::before {
        margin-right: 0.5rem;
    }
    
    .divider::after {
        margin-left: 0.5rem;
    }
    
    .demo-credentials {
        background: rgba(0, 173, 181, 0.1);
        border-radius: 10px;
        padding: 0.8rem;
        margin-top: 1.5rem;
        font-size: 0.75rem;
        color: #888;
    }
    
    .stButton > button {
        width: 100%;
        background: #00adb5 !important;
        color: white !important;
        border: none;
        border-radius: 50px !important;
        padding: 0.6rem !important;
        font-weight: 500 !important;
    }
    
    .stTextInput input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 0.6rem !important;
    }
    
    hr {
        margin: 1rem 0;
        border: none;
        height: 1px;
        background: #334155;
    }
</style>
"""

# =====================================
# MAIN APP CSS
# =====================================
main_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    .main .block-container {
        background: rgba(18, 18, 30, 0.92);
        border-radius: 20px;
        padding: 2rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    *:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    h1 {
        text-align: center;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-bottom: 2rem;
    }
    
    .user-info {
        background: rgba(0, 173, 181, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 50px;
        display: inline-block;
        margin-bottom: 1rem;
        font-size: 0.8rem;
    }
    
    .stNumberInput label, .stSelectbox label {
        color: #cbd5e0 !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
    }
    
    .stNumberInput input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
    }
    
    .stNumberInput input:hover {
        border-color: #00adb5 !important;
    }
    
    .stNumberInput button {
        background-color: #2d2d44 !important;
    }
    
    .stNumberInput button:hover {
        background-color: #00adb5 !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #1a1a2e !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #00adb5 !important;
    }
    
    .stButton > button {
        width: 100%;
        background: #00adb5 !important;
        color: white !important;
        border: none;
        border-radius: 50px !important;
        padding: 0.6rem !important;
        font-weight: 600 !important;
    }
    
    .stButton > button:hover {
        background: #007a7f !important;
        transform: translateY(-2px);
    }
    
    .result-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 2px solid #00adb5;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
        animation: slideDown 0.4s ease-out;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-label {
        color: #888888 !important;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 3px;
    }
    
    .result-score {
        color: #00adb5 !important;
        font-size: 3.5rem;
        font-weight: 800;
    }
    
    .result-score span {
        font-size: 1.2rem;
        color: #666666 !important;
    }
    
    .stSuccess, .stInfo, .stWarning {
        border-radius: 12px;
        padding: 1rem;
        margin: 0.8rem 0;
    }
    
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: #334155;
    }
    
    div[data-testid="column"] {
        padding: 0 0.6rem;
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        h1 {
            font-size: 1.5rem !important;
        }
        .result-score {
            font-size: 2rem;
        }
    }
</style>
"""

# =====================================
# GOOGLE SIGN IN HANDLER
# =====================================
def google_sign_in(email, name):
    users = load_users()
    
    if email not in users:
        # New user - register
        users[email] = {
            "name": name,
            "email": email,
            "created_at": str(datetime.now())
        }
        save_users(users)
    
    st.session_state.logged_in = True
    st.session_state.username = name
    st.session_state.user_email = email
    st.rerun()

# =====================================
# LOGOUT FUNCTION
# =====================================
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_email = ""
    st.rerun()

# =====================================
# AUTH PAGE
# =====================================
def show_auth_page():
    st.markdown(auth_css, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-container">
        <div class="auth-title">Student Score Predictor</div>
        <div class="auth-subtitle">Sign in to continue</div>
    """, unsafe_allow_html=True)
    
    # Google Sign In Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Demo Google Sign In - In production, use actual OAuth
        st.markdown("""
        <button class="google-btn" onclick="alert('Demo Mode: Click OK to continue')">
            <svg width="20" height="20" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Sign in with Google
        </button>
        """, unsafe_allow_html=True)
    
    # Demo Sign In (for testing)
    st.markdown('<div class="divider">OR</div>', unsafe_allow_html=True)
    
    demo_email = st.text_input("Email", placeholder="your@email.com", key="demo_email")
    demo_name = st.text_input("Name", placeholder="Your name", key="demo_name")
    
    if st.button("Continue with Email", use_container_width=True):
        if demo_email and demo_name:
            google_sign_in(demo_email, demo_name)
        else:
            st.warning("Please enter email and name")
    
    st.markdown("""
        <div class="demo-credentials">
            Demo Mode: Enter any email and name to continue<br>
            No password required for demonstration
        </div>
    </div>
    """, unsafe_allow_html=True)

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
    st.markdown(main_css, unsafe_allow_html=True)
    
    # Top bar
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f'<div class="user-info">Welcome, {st.session_state.username}</div>', unsafe_allow_html=True)
    with col3:
        if st.button("Sign Out", key="logout_btn"):
            logout()
    
    st.markdown("<h1>Student Score Predictor</h1>", unsafe_allow_html=True)
    
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
                st.info(f"{rec}")
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
