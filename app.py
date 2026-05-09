import streamlit as st
import joblib
import pandas as pd
import numpy as np
import hashlib
import json
import os
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
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

def calculate_age(birth_date):
    today = datetime.now()
    age = today.year - birth_date.year
    if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
        age -= 1
    return age

# =====================================
# SESSION STATE
# =====================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_role' not in st.session_state:
    st.session_state.user_role = ""
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "login"
if 'signup_role' not in st.session_state:
    st.session_state.signup_role = "student"
if 'theme' not in st.session_state:
    st.session_state.theme = "dark"

# =====================================
# THEME CSS - FIX LIGHT MODE TEXT
# =====================================
light_theme_css = """
<style>
    .stApp { background: linear-gradient(135deg, #f5f7fa, #c3cfe2); }
    .main .block-container { background: rgba(255, 255, 255, 0.98); border-radius: 20px; padding: 1.5rem; border: 1px solid #e0e0e0; }
    [data-testid="stSidebar"] { background: rgba(255, 255, 255, 0.95); border-right: 1px solid #e0e0e0; }
    
    /* All text dark in light mode */
    h1, h2, h3, p, label, .stMarkdown, .auth-title, .stCaption, .footer-text {
        color: #1a1a2e !important;
    }
    
    /* Labels */
    .stNumberInput label, .stSelectbox label { color: #4a5568 !important; font-weight: 500 !important; transition: color 0.3s ease; }
    .stNumberInput label:hover, .stSelectbox label:hover { color: #00adb5 !important; }
    
    /* Input fields */
    .stNumberInput input, .stTextInput input, div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
        -webkit-text-fill-color: #1a1a2e !important;
        border: 1px solid #d0d0d0 !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
        font-size: 0.9rem !important;
        padding: 0.4rem 0.8rem !important;
    }
    .stNumberInput input:hover, .stTextInput input:hover, div[data-baseweb="select"] > div:hover {
        border-color: #00adb5 !important;
        transform: translateY(-1px);
    }
    
    /* Increase/Decrease buttons */
    .stNumberInput button {
        background-color: #e0e0e0 !important;
        border: 1px solid #c0c0c0 !important;
        color: #1a1a2e !important;
        transition: all 0.3s ease !important;
        border-radius: 6px !important;
        font-size: 0.8rem !important;
    }
    .stNumberInput button:hover {
        background-color: #00adb5 !important;
        color: white !important;
        transform: scale(1.05) !important;
        border-color: #00adb5 !important;
    }
    
    /* Result Card */
    .result-card { background: #ffffff; border: 2px solid #00adb5; border-radius: 20px; padding: 1.5rem; text-align: center; margin: 1.5rem 0; transition: all 0.3s ease; }
    .result-card:hover { transform: scale(1.02); box-shadow: 0 10px 30px rgba(0,173,181,0.2); }
    .result-score { color: #00adb5 !important; font-size: 2.5rem; font-weight: 800; }
    .result-label { color: #666666 !important; }
    
    /* Buttons */
    .stButton > button { background: #00adb5 !important; color: white !important; border: none; border-radius: 50px !important; padding: 0.5rem !important; font-weight: 600 !important; transition: all 0.3s ease; font-size: 0.9rem; }
    .stButton > button:hover { background: #007a7f !important; transform: translateY(-2px); }
    
    /* Dropdown */
    div[data-baseweb="popover"] > div { background-color: #ffffff !important; border: 1px solid #d0d0d0 !important; border-radius: 10px !important; }
    li[role="option"] { color: #1a1a2e !important; background-color: #ffffff !important; transition: all 0.2s ease; }
    li[role="option"]:hover { background-color: #00adb5 !important; color: white !important; transform: translateX(5px); }
    
    /* Sidebar text */
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: #1a1a2e !important; }
    
    .stSuccess, .stInfo, .stWarning { background-color: rgba(0, 173, 181, 0.1) !important; color: #1a1a2e !important; border-radius: 10px; }
    hr { background: #d0d0d0 !important; }
    .footer-text { color: #666666 !important; }
    
    /* Auth container */
    .auth-container { background: rgba(255, 255, 255, 0.98); border: 1px solid #e0e0e0; }
    .role-login-hint { background: rgba(0,173,181,0.1); color: #1a1a2e; }
    input::placeholder { color: #999999 !important; }
</style>
"""

dark_theme_css = """
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
    .main .block-container { background: rgba(18, 18, 30, 0.95); border-radius: 20px; padding: 1.5rem; border: 1px solid #334155; }
    [data-testid="stSidebar"] { background: rgba(18, 18, 30, 0.95); border-right: 1px solid #334155; }
    
    h1, h2, h3, p, label, .stMarkdown, .auth-title, .stCaption, .footer-text {
        color: #ffffff !important;
    }
    
    .stNumberInput label, .stSelectbox label { color: #cbd5e0 !important; }
    .stNumberInput label:hover, .stSelectbox label:hover { color: #00adb5 !important; }
    
    .stNumberInput input, .stTextInput input, div[data-baseweb="select"] > div {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        font-size: 0.9rem !important;
        padding: 0.4rem 0.8rem !important;
    }
    .stNumberInput input:hover, .stTextInput input:hover, div[data-baseweb="select"] > div:hover {
        border-color: #00adb5 !important;
        transform: translateY(-1px);
    }
    
    .stNumberInput button {
        background-color: #2d2d44 !important;
        border: 1px solid #334155 !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
        border-radius: 6px !important;
        font-size: 0.8rem !important;
    }
    .stNumberInput button:hover {
        background-color: #00adb5 !important;
        transform: scale(1.05) !important;
        border-color: #00adb5 !important;
    }
    
    .result-card { background: linear-gradient(135deg, #1a1a2e, #16213e); border: 2px solid #00adb5; border-radius: 20px; padding: 1.5rem; text-align: center; margin: 1.5rem 0; transition: all 0.3s ease; }
    .result-card:hover { transform: scale(1.02); box-shadow: 0 10px 30px rgba(0,173,181,0.3); }
    .result-score { color: #00adb5 !important; font-size: 2.5rem; font-weight: 800; }
    .result-label { color: #888888 !important; }
    
    .stButton > button { background: #00adb5 !important; color: white !important; border: none; border-radius: 50px !important; padding: 0.5rem !important; font-weight: 600 !important; transition: all 0.3s ease; font-size: 0.9rem; }
    .stButton > button:hover { background: #007a7f !important; transform: translateY(-2px); }
    
    div[data-baseweb="popover"] > div { background-color: #1a1a2e !important; border: 1px solid #334155 !important; }
    li[role="option"] { color: #ffffff !important; background-color: #1a1a2e !important; }
    li[role="option"]:hover { background-color: #00adb5 !important; transform: translateX(5px); }
    
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: #ffffff !important; }
    
    .stSuccess, .stInfo, .stWarning { background-color: rgba(0, 173, 181, 0.2) !important; color: #ffffff !important; }
    hr { background: #334155 !important; }
    .footer-text { color: #888888 !important; }
    
    .auth-container { background: rgba(18, 18, 30, 0.95); border: 1px solid #334155; }
    .role-login-hint { background: rgba(0,173,181,0.2); color: #ffffff; }
    input::placeholder { color: #888888 !important; }
</style>
"""

base_css = """
<style>
    *:focus { outline: none !important; box-shadow: none !important; }
    div[data-testid="column"] { padding: 0 0.5rem; }
    .auth-container { max-width: 420px; margin: 60px auto; text-align: center; padding: 2rem; border-radius: 20px; }
    .auth-title { font-size: 1.5rem; font-weight: 700; margin-bottom: 0.5rem; }
    .role-login-hint { font-size: 0.75rem; margin-top: -0.5rem; margin-bottom: 0.8rem; padding: 0.3rem 0.6rem; border-radius: 8px; display: inline-block; }
    hr { margin: 1rem 0; border: none; height: 1px; }
    .footer-text { margin-top: 1rem; font-size: 0.7rem; }
    
    /* Sidebar Profile Card */
    .profile-card { text-align: center; padding: 0.5rem; border-radius: 15px; margin-bottom: 1rem; }
    .profile-name { font-size: 1.1rem; font-weight: 700; margin: 0.3rem 0; }
    .profile-role { font-size: 0.7rem; padding: 0.2rem 0.6rem; border-radius: 50px; display: inline-block; }
    .profile-detail { font-size: 0.7rem; margin: 0.2rem 0; opacity: 0.8; }
    
    /* Top right theme toggle */
    .top-theme-toggle {
        position: fixed;
        top: 0.7rem;
        right: 1rem;
        z-index: 999;
    }
    .top-theme-toggle button {
        background: rgba(0, 173, 181, 0.2) !important;
        border: 1px solid #00adb5 !important;
        border-radius: 50px !important;
        padding: 0.2rem 0.8rem !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }
    
    @media (max-width: 768px) {
        .main .block-container { padding: 1rem; }
        h1 { font-size: 1.3rem !important; }
        .result-score { font-size: 2rem; }
        .top-theme-toggle button { padding: 0.15rem 0.5rem !important; font-size: 0.7rem !important; }
    }
</style>
"""

def apply_theme():
    if st.session_state.theme == "dark":
        st.markdown(dark_theme_css, unsafe_allow_html=True)
    else:
        st.markdown(light_theme_css, unsafe_allow_html=True)
    st.markdown(base_css, unsafe_allow_html=True)

# =====================================
# AUTH PAGE
# =====================================
def show_auth_page():
    apply_theme()
    
    # Top right theme toggle
    st.markdown('<div class="top-theme-toggle">', unsafe_allow_html=True)
    mode_text = "Dark" if st.session_state.theme == "light" else "Light"
    mode_icon = "🌙" if st.session_state.theme == "light" else "☀️"
    if st.button(f"{mode_icon} {mode_text} Mode", key="theme_toggle_auth"):
        if st.session_state.theme == "dark":
            st.session_state.theme = "light"
        else:
            st.session_state.theme = "dark"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    users = load_users()
    
    st.markdown("""
    <div class="auth-container">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎓</div>
        <div class="auth-title">Student Score Predictor</div>
    """, unsafe_allow_html=True)
    
    if st.session_state.auth_mode == "login":
        st.markdown('<p style="margin-bottom: 1rem;">Sign in to your account</p>', unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Username", key="login_username")
        password = st.text_input("Password", type="password", placeholder="Password", key="login_password")
        
        if username and username in users:
            role = users[username]["role"]
            role_icon = "👨‍🎓" if role == "student" else "👨‍👩‍👧"
            role_text = "Student" if role == "student" else "Parent"
            st.markdown(f'<div class="role-login-hint">{role_icon} Login as: <strong>{role_text}</strong></div>', unsafe_allow_html=True)
        
        if st.button("Sign In", use_container_width=True):
            if username and password:
                if username in users and users[username]["password"] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_role = users[username]["role"]
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.warning("Please enter username and password")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sign Up as Student", use_container_width=True):
                st.session_state.auth_mode = "signup"
                st.session_state.signup_role = "student"
                st.rerun()
        with col2:
            if st.button("Sign Up as Parent", use_container_width=True):
                st.session_state.auth_mode = "signup"
                st.session_state.signup_role = "parent"
                st.rerun()
    
    else:
        role = st.session_state.signup_role
        st.markdown(f'<p style="margin-bottom: 1rem;">Create account as <strong>{role.upper()}</strong></p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Student", use_container_width=True):
                st.session_state.signup_role = "student"
                st.rerun()
        with col2:
            if st.button("Parent", use_container_width=True):
                st.session_state.signup_role = "parent"
                st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Username", key="signup_username")
        password = st.text_input("Password", type="password", placeholder="Password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm Password", key="signup_confirm")
        full_name = st.text_input("Full Name", placeholder="Full Name", key="signup_name")
        
        if role == "student":
            dob = st.date_input("Date of Birth", min_value=datetime(1990, 1, 1), max_value=datetime.now(), key="student_dob")
            grade = st.selectbox("Current Grade/Class", ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12", "College"])
            school = st.text_input("School Name", placeholder="School Name", key="student_school")
        else:
            child_name = st.text_input("Child's Name", placeholder="Child's Name", key="parent_child")
            child_dob = st.date_input("Child's Date of Birth", min_value=datetime(1990, 1, 1), max_value=datetime.now(), key="parent_dob")
            child_grade = st.selectbox("Child's Grade/Class", ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12", "College"])
            relation = st.selectbox("Relationship", ["Father", "Mother", "Guardian"])
        
        if st.button("Create Account", use_container_width=True):
            if not username or not password or not full_name:
                st.warning("Please fill all required fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 4:
                st.warning("Password must be at least 4 characters")
            elif username in users:
                st.error("Username already exists")
            else:
                user_data = {
                    "password": hash_password(password),
                    "role": role,
                    "full_name": full_name,
                    "created_at": str(pd.Timestamp.now())
                }
                if role == "student":
                    user_data["dob"] = str(dob)
                    user_data["age"] = calculate_age(dob)
                    user_data["grade"] = grade
                    user_data["school"] = school
                else:
                    user_data["child_name"] = child_name
                    user_data["child_dob"] = str(child_dob)
                    user_data["child_age"] = calculate_age(child_dob)
                    user_data["child_grade"] = child_grade
                    user_data["relation"] = relation
                
                users[username] = user_data
                save_users(users)
                st.success(f"Account created successfully as {role}!")
                st.session_state.auth_mode = "login"
                st.rerun()
        
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("Back to Sign In", use_container_width=True):
            st.session_state.auth_mode = "login"
            st.rerun()
    
    st.markdown('<div class="footer-text">Secure • Free • Student & Parent Portals</div>', unsafe_allow_html=True)
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
# SIDEBAR DASHBOARD (NO THEME TOGGLE HERE)
# =====================================
def show_sidebar(user_data):
    with st.sidebar:
        st.markdown("---")
        
        role_text = "Student" if st.session_state.user_role == "student" else "Parent"
        role_icon = "👨‍🎓" if st.session_state.user_role == "student" else "👨‍👩‍👧"
        
        st.markdown(f"""
        <div class="profile-card">
            <div style="font-size: 2rem;">{role_icon}</div>
            <div class="profile-name">{user_data.get('full_name', st.session_state.username)}</div>
            <div class="profile-role" style="background: {'#00adb5' if st.session_state.user_role == 'student' else '#9c27b0'}20; border: 1px solid {'#00adb5' if st.session_state.user_role == 'student' else '#9c27b0'};">{role_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Profile Details")
        st.markdown(f"**Username:** {st.session_state.username}")
        
        if st.session_state.user_role == "student":
            st.markdown(f"**Full Name:** {user_data.get('full_name', 'N/A')}")
            st.markdown(f"**Age:** {user_data.get('age', 'N/A')} years")
            st.markdown(f"**Grade:** {user_data.get('grade', 'N/A')}")
            st.markdown(f"**School:** {user_data.get('school', 'N/A')}")
        else:
            st.markdown(f"**Parent Name:** {user_data.get('full_name', 'N/A')}")
            st.markdown(f"**Relationship:** {user_data.get('relation', 'N/A')}")
            st.markdown(f"**Child Name:** {user_data.get('child_name', 'N/A')}")
            st.markdown(f"**Child Age:** {user_data.get('child_age', 'N/A')} years")
            st.markdown(f"**Child Grade:** {user_data.get('child_grade', 'N/A')}")
        
        st.markdown("---")
        
        # Sign Out Button in Sidebar
        if st.button("🚪 Sign Out", use_container_width=True, key="logout_btn_sidebar"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_role = ""
            st.rerun()
        
        st.caption("Student Score Predictor v2.0")

# =====================================
# MAIN APP
# =====================================
def show_main_app():
    apply_theme()
    
    # Top right theme toggle (outside sidebar)
    st.markdown('<div class="top-theme-toggle">', unsafe_allow_html=True)
    mode_text = "Dark" if st.session_state.theme == "light" else "Light"
    mode_icon = "🌙" if st.session_state.theme == "light" else "☀️"
    if st.button(f"{mode_icon} {mode_text} Mode", key="theme_toggle_main"):
        if st.session_state.theme == "dark":
            st.session_state.theme = "light"
        else:
            st.session_state.theme = "dark"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    users = load_users()
    user_data = users.get(st.session_state.username, {})
    
    # Sidebar
    show_sidebar(user_data)
    
    # Main Content - No duplicate profile info
    st.markdown("<h1 style='text-align: center;'>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)
    
    # Only show child info for parent (but concise, no duplicate)
    if st.session_state.user_role == "parent":
        child_name = user_data.get("child_name", "Not specified")
        st.info(f"👨‍👩‍👧 Predicting for: **{child_name}**")
    
    model, columns = load_models()
    
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
        
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">PREDICTED EXAM SCORE</div>
            <div class="result-score">{final_score}<span> / 100</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        if final_score >= 85:
            st.success("🏆 Exceptional Performance")
            st.balloons()
        elif final_score >= 70:
            st.success("📈 Good Performance")
        elif final_score >= 55:
            st.info("📚 Satisfactory Performance")
        else:
            st.warning("⚠️ Needs Improvement")
        
        recommendations = []
        if hours < 6:
            recommendations.append("📖 Increase study hours to 6-8 hours daily")
        if attendance < 75:
            recommendations.append("📊 Improve attendance to 80% or higher")
        if sleep < 7:
            recommendations.append("😴 Get 7-9 hours of sleep for better focus")
        if motivation == "Low":
            recommendations.append("💪 Set daily goals to boost motivation")
        if teacher == "Poor":
            recommendations.append("👨‍🏫 Seek additional tutoring or online resources")
        if resources == "Low":
            recommendations.append("📚 Utilize free online learning materials")
        if peer == "Negative":
            recommendations.append("🤝 Join positive study groups")
        
        if recommendations:
            st.markdown("### 💡 Recommendations")
            for rec in recommendations:
                st.info(rec)
        else:
            st.success("✅ Excellent study habits. Maintain your routine")
    
    st.markdown("---")
    st.caption("Student Score Predictor | Powered by Machine Learning")

# =====================================
# MAIN ROUTER
# =====================================
if st.session_state.logged_in:
    show_main_app()
else:
    show_auth_page()
