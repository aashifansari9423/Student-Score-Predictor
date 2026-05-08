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
    """Load users from JSON file"""
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_user_exists(username, users):
    """Check if username already exists"""
    return username in users

def register_user(username, password, users):
    """Register new user"""
    if check_user_exists(username, users):
        return False, "Username already exists!"
    users[username] = {
        "password": hash_password(password),
        "created_at": str(pd.Timestamp.now())
    }
    save_users(users)
    return True, "Registration successful!"

def login_user(username, password, users):
    """Authenticate user"""
    if username not in users:
        return False, "Username not found!"
    if users[username]["password"] != hash_password(password):
        return False, "Incorrect password!"
    return True, "Login successful!"

# =====================================
# SESSION STATE
# =====================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "login"  # login or signup

# =====================================
# AUTH PAGES CSS
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
        max-width: 450px;
        margin: 50px auto;
        border: 1px solid #334155;
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .auth-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .auth-icon {
        text-align: center;
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .auth-footer {
        text-align: center;
        margin-top: 1.5rem;
        color: #666;
        font-size: 0.8rem;
    }
    
    .switch-mode {
        text-align: center;
        margin-top: 1rem;
    }
    
    .switch-mode button {
        background: transparent !important;
        color: #00adb5 !important;
        border: none !important;
        text-decoration: underline;
    }
    
    .stTextInput input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 0.6rem !important;
    }
    
    .stTextInput input:focus {
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
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #007a7f !important;
        transform: translateY(-2px);
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
# LOGIN/SIGNUP PAGE
# =====================================
def show_auth_page():
    st.markdown(auth_css, unsafe_allow_html=True)
    
    users = load_users()
    
    # Auth mode toggle
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 SIGN IN", use_container_width=True, type="primary" if st.session_state.auth_mode == "login" else "secondary"):
            st.session_state.auth_mode = "login"
            st.rerun()
    with col2:
        if st.button("📝 SIGN UP", use_container_width=True, type="primary" if st.session_state.auth_mode == "signup" else "secondary"):
            st.session_state.auth_mode = "signup"
            st.rerun()
    
    st.markdown("---")
    
    if st.session_state.auth_mode == "login":
        # SIGN IN FORM
        st.markdown("""
        <div class="auth-container">
            <div class="auth-icon">🎓</div>
            <div class="auth-title">Welcome Back!</div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter your username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        if st.button("SIGN IN", use_container_width=True):
            if username and password:
                success, message = login_user(username, password, users)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.warning("Please enter username and password")
        
        st.markdown("""
            <div class="auth-footer">
                New to Student Score Predictor?<br>
                Click <strong>SIGN UP</strong> to create an account
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # SIGN UP FORM
        st.markdown("""
        <div class="auth-container">
            <div class="auth-icon">📝</div>
            <div class="auth-title">Create Account</div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
        password = st.text_input("Password", type="password", placeholder="Choose a password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="signup_confirm")
        
        if st.button("CREATE ACCOUNT", use_container_width=True):
            if not username or not password:
                st.warning("Please fill all fields")
            elif password != confirm_password:
                st.error("Passwords do not match!")
            elif len(password) < 4:
                st.warning("Password must be at least 4 characters")
            else:
                success, message = register_user(username, password, users)
                if success:
                    st.success(message)
                    st.info("Please sign in with your new account")
                    st.session_state.auth_mode = "login"
                    st.rerun()
                else:
                    st.error(message)
        
        st.markdown("""
            <div class="auth-footer">
                Already have an account?<br>
                Click <strong>SIGN IN</strong> to login
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
# LOGOUT FUNCTION
# =====================================
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# =====================================
# MAIN APP
# =====================================
def show_main_app():
    st.markdown(main_css, unsafe_allow_html=True)
    
    # Top bar
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f'<div class="user-info">👤 Welcome, <strong>{st.session_state.username}</strong>!</div>', unsafe_allow_html=True)
    with col3:
        if st.button("🚪 LOGOUT", key="logout_btn"):
            logout()
    
    st.markdown("<h1>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)
    
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
    if st.button("PREDICT SCORE", use_container_width=True):
        
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
            st.success("🏆 EXCEPTIONAL PERFORMANCE")
            st.balloons()
        elif final_score >= 70:
            st.success("📈 GOOD PERFORMANCE")
        elif final_score >= 55:
            st.info("📚 SATISFACTORY PERFORMANCE")
        else:
            st.warning("⚠️ NEEDS IMPROVEMENT")
        
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
                st.info(f"• {rec}")
        else:
            st.success("✅ Excellent study habits! Maintain your routine")
    
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
