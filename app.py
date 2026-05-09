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
# PROFESSIONAL CSS
# =====================================
light_theme_css = """
<style>
    /* Global Reset */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Main App */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main Container */
    .main .block-container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 24px;
        padding: 1.8rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        backdrop-filter: blur(0px);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #eef2f6;
        box-shadow: 2px 0 12px rgba(0,0,0,0.02);
    }
    
    [data-testid="stSidebar"] * {
        color: #2d3748;
    }
    
    /* Typography */
    h1 {
        font-size: 2rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem !important;
        text-align: center;
        letter-spacing: -0.5px;
    }
    
    h2, h3 {
        color: #2d3748 !important;
        font-weight: 600 !important;
        letter-spacing: -0.3px;
    }
    
    p, label, .stMarkdown {
        color: #4a5568 !important;
    }
    
    /* Input Fields - Modern */
    .stNumberInput input, .stTextInput input {
        background: #ffffff !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 0.6rem 1rem !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        color: #1a202c !important;
    }
    
    .stNumberInput input:focus, .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102,126,234,0.1) !important;
        outline: none;
    }
    
    /* Select Box - Professional */
    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 12px !important;
        min-height: 42px !important;
        transition: all 0.2s ease !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #667eea !important;
    }
    
    div[data-baseweb="select"] input {
        color: #1a202c !important;
        font-size: 0.9rem !important;
    }
    
    /* Number Buttons */
    .stNumberInput button {
        background: #f7fafc !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        color: #4a5568 !important;
    }
    
    .stNumberInput button:hover {
        background: #667eea !important;
        border-color: #667eea !important;
        color: white !important;
        transform: scale(1.02);
    }
    
    /* Dropdown Menu */
    div[data-baseweb="popover"] div {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
    }
    
    li[role="option"] {
        color: #2d3748 !important;
        padding: 10px 14px !important;
        transition: all 0.15s ease !important;
        border-radius: 8px !important;
        margin: 2px 4px !important;
    }
    
    li[role="option"]:hover {
        background: #667eea !important;
        color: white !important;
        transform: translateX(4px);
    }
    
    /* Result Card - Premium */
    .result-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(102,126,234,0.25);
        transition: all 0.3s ease;
    }
    
    .result-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(102,126,234,0.3);
    }
    
    .result-label {
        color: rgba(255,255,255,0.8) !important;
        font-size: 0.7rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .result-score {
        color: white !important;
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    .result-score span {
        font-size: 1rem;
        font-weight: 400;
        opacity: 0.8;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease !important;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102,126,234,0.3);
    }
    
    /* Theme Toggle */
    .top-theme-toggle {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
    }
    
    .top-theme-toggle button {
        background: rgba(255,255,255,0.2) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 40px !important;
        padding: 0.4rem 1rem !important;
        font-size: 0.75rem !important;
        font-weight: 500 !important;
        color: white !important;
    }
    
    .top-theme-toggle button:hover {
        background: rgba(255,255,255,0.3) !important;
        transform: translateY(-2px);
    }
    
    /* Profile Card */
    .profile-card {
        text-align: center;
        padding: 1rem 0.5rem;
        background: linear-gradient(135deg, #f7fafc, #edf2f7);
        border-radius: 20px;
        margin-bottom: 1rem;
    }
    
    .profile-name {
        font-size: 1rem;
        font-weight: 700;
        color: #2d3748;
        margin-top: 0.3rem;
    }
    
    .profile-role {
        font-size: 0.65rem;
        padding: 0.2rem 0.8rem;
        border-radius: 30px;
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white !important;
        font-weight: 500;
    }
    
    /* Info/Warning/Success */
    .stInfo, .stSuccess, .stWarning {
        border-radius: 14px !important;
        border-left: 4px solid !important;
        padding: 0.8rem 1rem !important;
    }
    
    .stInfo { background: rgba(102,126,234,0.08) !important; border-left-color: #667eea !important; }
    .stSuccess { background: rgba(72,187,120,0.08) !important; border-left-color: #48bb78 !important; }
    .stWarning { background: rgba(237,137,54,0.08) !important; border-left-color: #ed8936 !important; }
    
    hr {
        margin: 1rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    }
    
    /* Auth Container */
    .auth-container {
        background: white;
        border-radius: 28px;
        padding: 2rem;
        box-shadow: 0 25px 50px rgba(0,0,0,0.08);
        text-align: center;
    }
    
    /* Placeholder */
    input::placeholder {
        color: #a0aec0 !important;
        font-size: 0.85rem;
    }
</style>
"""

dark_theme_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    .main .block-container {
        background: rgba(18, 18, 30, 0.92);
        border-radius: 24px;
        padding: 1.8rem;
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(0px);
    }
    
    [data-testid="stSidebar"] {
        background: rgba(18, 18, 30, 0.95);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    
    h1 {
        background: linear-gradient(135deg, #a78bfa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    h2, h3, p, label, .stMarkdown {
        color: #e2e8f0 !important;
    }
    
    .stNumberInput input, .stTextInput input {
        background: #1a1a2e !important;
        border: 1.5px solid #2d2d44 !important;
        color: #ffffff !important;
    }
    
    .stNumberInput input:focus, .stTextInput input:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 3px rgba(167,139,250,0.2) !important;
    }
    
    div[data-baseweb="select"] > div {
        background: #1a1a2e !important;
        border: 1.5px solid #2d2d44 !important;
    }
    
    div[data-baseweb="select"] input {
        color: #ffffff !important;
    }
    
    .stNumberInput button {
        background: #2d2d44 !important;
        border: 1px solid #3d3d5a !important;
        color: #ffffff !important;
    }
    
    .stNumberInput button:hover {
        background: #a78bfa !important;
        border-color: #a78bfa !important;
    }
    
    div[data-baseweb="popover"] div {
        background: #1a1a2e !important;
        border: 1px solid #2d2d44 !important;
    }
    
    li[role="option"] {
        color: #e2e8f0 !important;
    }
    
    li[role="option"]:hover {
        background: #a78bfa !important;
    }
    
    .result-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid rgba(167,139,250,0.3);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #a78bfa, #c084fc) !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 20px rgba(167,139,250,0.4);
    }
    
    .top-theme-toggle button {
        background: rgba(255,255,255,0.1) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
    }
    
    .profile-card {
        background: rgba(255,255,255,0.05);
    }
    
    .profile-name {
        color: #e2e8f0;
    }
    
    .profile-role {
        background: linear-gradient(135deg, #a78bfa, #c084fc);
        color: white !important;
    }
    
    hr {
        background: linear-gradient(90deg, transparent, #2d2d44, transparent);
    }
    
    .auth-container {
        background: rgba(18, 18, 30, 0.95);
        border: 1px solid rgba(255,255,255,0.08);
    }
    
    input::placeholder {
        color: #94a3b8 !important;
    }
</style>
"""

def apply_theme():
    if st.session_state.theme == "dark":
        st.markdown(dark_theme_css, unsafe_allow_html=True)
    else:
        st.markdown(light_theme_css, unsafe_allow_html=True)

def theme_toggle():
    mode_text = "Light" if st.session_state.theme == "dark" else "Dark"
    mode_icon = "☀️" if st.session_state.theme == "dark" else "🌙"
    if st.button(f"{mode_icon} {mode_text}", key="theme_toggle"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()

# =====================================
# AUTH PAGE
# =====================================
def show_auth_page():
    apply_theme()
    
    st.markdown('<div class="top-theme-toggle">', unsafe_allow_html=True)
    theme_toggle()
    st.markdown('</div>', unsafe_allow_html=True)
    
    users = load_users()
    
    col1, col2, col3 = st.columns([1, 2.2, 1])
    
    with col2:
        st.markdown("""
        <div class="auth-container">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🎓</div>
            <h1 style="font-size: 1.8rem; margin: 0;">Student Score Predictor</h1>
        """, unsafe_allow_html=True)
        
        if st.session_state.auth_mode == "login":
            st.markdown('<p style="text-align: center; margin-bottom: 1.5rem; margin-top: 0.5rem;">Sign in to continue</p>', unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="Username", key="login_user", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Password", key="login_pass", label_visibility="collapsed")
            
            if username and username in users:
                role = users[username]["role"]
                role_icon = "🎓" if role == "student" else "👨‍👩‍👧"
                role_text = "Student" if role == "student" else "Parent"
                st.markdown(f'<p style="text-align: center; font-size: 0.7rem; margin-top: -0.3rem;">{role_icon} {role_text}</p>', unsafe_allow_html=True)
            
            if st.button("Sign In", use_container_width=True):
                if username and password:
                    if username in users and users[username]["password"] == hash_password(password):
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_role = users[username]["role"]
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
                else:
                    st.warning("Enter username and password")
            
            st.markdown("<hr>", unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Student Sign Up", use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.session_state.signup_role = "student"
                    st.rerun()
            with col_b:
                if st.button("Parent Sign Up", use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.session_state.signup_role = "parent"
                    st.rerun()
        
        else:
            role = st.session_state.signup_role
            st.markdown(f'<p style="text-align: center; margin-bottom: 0.8rem; margin-top: 0.5rem;">Create {role} account</p>', unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Student", use_container_width=True):
                    st.session_state.signup_role = "student"
                    st.rerun()
            with col_b:
                if st.button("Parent", use_container_width=True):
                    st.session_state.signup_role = "parent"
                    st.rerun()
            
            st.markdown("---")
            
            username = st.text_input("Username", placeholder="Username", key="signup_user", label_visibility="collapsed")
            password = st.text_input("Password", type="password", placeholder="Password", key="signup_pass", label_visibility="collapsed")
            confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm", key="signup_confirm", label_visibility="collapsed")
            full_name = st.text_input("Full Name", placeholder="Full Name", key="signup_name", label_visibility="collapsed")
            
            if role == "student":
                dob = st.date_input("Date of Birth", min_value=datetime(1990,1,1), max_value=datetime.now())
                grade = st.selectbox("Grade", ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12", "College"])
                school = st.text_input("School Name", placeholder="School Name")
            else:
                child_name = st.text_input("Child's Name", placeholder="Child's Name")
                child_dob = st.date_input("Child's DOB", min_value=datetime(1990,1,1), max_value=datetime.now())
                child_grade = st.selectbox("Child's Grade", ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12", "College"])
                relation = st.selectbox("Relationship", ["Father", "Mother", "Guardian"])
            
            if st.button("Create Account", use_container_width=True):
                if not username or not password or not full_name:
                    st.warning("Fill all fields")
                elif password != confirm:
                    st.error("Passwords don't match")
                elif len(password) < 4:
                    st.warning("Password min 4 chars")
                elif username in users:
                    st.error("Username exists")
                else:
                    data = {
                        "password": hash_password(password),
                        "role": role,
                        "full_name": full_name,
                        "created_at": str(pd.Timestamp.now())
                    }
                    if role == "student":
                        data["dob"] = str(dob)
                        data["age"] = calculate_age(dob)
                        data["grade"] = grade
                        data["school"] = school
                    else:
                        data["child_name"] = child_name
                        data["child_dob"] = str(child_dob)
                        data["child_age"] = calculate_age(child_dob)
                        data["child_grade"] = child_grade
                        data["relation"] = relation
                    
                    users[username] = data
                    save_users(users)
                    st.success("Account created successfully!")
                    st.session_state.auth_mode = "login"
                    st.rerun()
            
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.button("← Back to Sign In", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()
        
        st.markdown('<p style="text-align: center; font-size: 0.6rem; opacity: 0.6;">Secure Portal for Students & Parents</p>', unsafe_allow_html=True)
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
# SIDEBAR
# =====================================
def show_sidebar(user_data):
    with st.sidebar:
        st.markdown("---")
        role_text = "Student" if st.session_state.user_role == "student" else "Parent"
        role_icon = "🎓" if st.session_state.user_role == "student" else "👨‍👩‍👧"
        
        st.markdown(f"""
        <div class="profile-card">
            <div style="font-size: 2rem;">{role_icon}</div>
            <div class="profile-name">{user_data.get('full_name', st.session_state.username)}</div>
            <div class="profile-role">{role_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Account Details")
        st.markdown(f"**Username:** {st.session_state.username}")
        st.markdown(f"**Name:** {user_data.get('full_name', 'N/A')}")
        
        if st.session_state.user_role == "student":
            st.markdown(f"**Age:** {user_data.get('age', 'N/A')}")
            st.markdown(f"**Grade:** {user_data.get('grade', 'N/A')}")
        else:
            st.markdown(f"**Child:** {user_data.get('child_name', 'N/A')}")
            st.markdown(f"**Child Grade:** {user_data.get('child_grade', 'N/A')}")
        
        st.markdown("---")
        
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.user_role = ""
            st.rerun()

# =====================================
# MAIN APP
# =====================================
def show_main_app():
    apply_theme()
    
    st.markdown('<div class="top-theme-toggle">', unsafe_allow_html=True)
    theme_toggle()
    st.markdown('</div>', unsafe_allow_html=True)
    
    users = load_users()
    user_data = users.get(st.session_state.username, {})
    
    show_sidebar(user_data)
    
    st.markdown("<h1>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)
    
    if st.session_state.user_role == "parent":
        child_name = user_data.get("child_name", "Child")
        st.info(f"👨‍👩‍👧 You are predicting for: **{child_name}**")
    
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
        
        recs = []
        if hours < 6: recs.append("📖 Increase study hours to 6-8 daily")
        if attendance < 75: recs.append("📊 Improve attendance to 80%+")
        if sleep < 7: recs.append("😴 Get 7-9 hours of sleep")
        if motivation == "Low": recs.append("💪 Set daily goals")
        if teacher == "Poor": recs.append("👨‍🏫 Seek tutoring")
        if resources == "Low": recs.append("📚 Use online resources")
        if peer == "Negative": recs.append("🤝 Join positive study groups")
        
        if recs:
            st.markdown("### Recommendations")
            for r in recs: st.info(r)
        else:
            st.success("✅ Excellent habits! Keep going!")
    
    st.markdown("---")
    st.caption("© 2024 Student Score Predictor | AI-Powered Academic Tool")

# =====================================
# MAIN
# =====================================
if st.session_state.logged_in:
    show_main_app()
else:
    show_auth_page()
