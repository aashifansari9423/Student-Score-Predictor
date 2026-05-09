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
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# =====================================
# CSS
# =====================================
light_theme_css = """
<style>
    .stApp, .stApp * {
        color: #1a1a2e !important;
    }
    .result-card .result-score {
        color: #00adb5 !important;
        font-weight: 800 !important;
        font-size: 2.2rem !important;
    }
    .result-card .result-label {
        color: #888 !important;
        font-size: 0.7rem !important;
        letter-spacing: 2px !important;
    }
    input::placeholder { color: #999 !important; }
    .stButton > button, .stButton > button * { color: white !important; }
    .top-theme-toggle button { color: #1a1a2e !important; }
    .profile-role { color: #1a1a2e !important; }
    
    .stApp { background: linear-gradient(135deg, #e0eafc, #cfdef3); }
    .main .block-container { background: #ffffff; border-radius: 20px; padding: 1.5rem; }
    [data-testid="stSidebar"] { background: #f8f9fa; border-right: 1px solid #e0e0e0; }
    
    .stNumberInput input, .stTextInput input {
        background: white !important;
        border: 1px solid #ddd !important;
        border-radius: 10px !important;
        padding: 0.4rem 0.8rem !important;
    }
    
    div[data-baseweb="select"] > div {
        background: white !important;
        border: 1px solid #ddd !important;
        border-radius: 10px !important;
        min-height: 38px !important;
    }
    
    .stNumberInput button {
        background: #f0f0f0 !important;
        border: 1px solid #ddd !important;
    }
    .stNumberInput button:hover {
        background: #00adb5 !important;
    }
    
    div[data-baseweb="popover"] div {
        background: white !important;
        border: 1px solid #ddd !important;
    }
    li[role="option"]:hover {
        background: #00adb5 !important;
    }
    
    .result-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 2px solid #00adb5;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: #00adb5 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.4rem 1rem !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,173,181,0.4);
    }
    
    .top-theme-toggle {
        position: fixed;
        top: 0.8rem;
        right: 1rem;
        z-index: 999;
    }
    .top-theme-toggle button {
        background: rgba(0,173,181,0.15) !important;
        border: 1px solid #00adb5 !important;
        border-radius: 50px !important;
        padding: 0.2rem 0.7rem !important;
        font-size: 0.7rem !important;
    }
    
    .profile-card { text-align: center; padding: 0.5rem; }
    .profile-name { font-size: 1rem; font-weight: 700; }
    .profile-role { font-size: 0.65rem; padding: 0.2rem 0.6rem; border-radius: 50px; display: inline-block; background: #00adb520; border: 1px solid #00adb5; }
    
    .stInfo, .stSuccess, .stWarning {
        background-color: rgba(0,173,181,0.1) !important;
    }
    
    hr { margin: 0.8rem 0; border-color: #eee; }
</style>
"""

dark_theme_css = """
<style>
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
    .main .block-container { background: rgba(18, 18, 30, 0.95); border-radius: 20px; padding: 1.5rem; border: 1px solid #2a2a4a; }
    [data-testid="stSidebar"] { background: rgba(18, 18, 30, 0.95); border-right: 1px solid #2a2a4a; }
    
    h1, h2, h3, p, label, .stMarkdown, .stCaption { color: #ffffff !important; }
    
    .result-card .result-label { color: #888 !important; font-size: 0.7rem !important; letter-spacing: 2px !important; }
    .result-card .result-score { color: #00adb5 !important; font-weight: 800 !important; font-size: 2.2rem !important; }
    
    .stNumberInput input, .stTextInput input {
        background: #1e1e2e !important;
        border: 1px solid #3a3a5a !important;
        border-radius: 10px !important;
        padding: 0.4rem 0.8rem !important;
        color: #ffffff !important;
    }
    
    div[data-baseweb="select"] > div {
        background: #1e1e2e !important;
        border: 1px solid #3a3a5a !important;
        border-radius: 10px !important;
        min-height: 38px !important;
    }
    div[data-baseweb="select"] input {
        color: #ffffff !important;
    }
    
    .stNumberInput button {
        background: #2d2d44 !important;
        border: 1px solid #3a3a5a !important;
        color: #ffffff !important;
    }
    .stNumberInput button:hover {
        background: #00adb5 !important;
    }
    
    div[data-baseweb="popover"] div {
        background: #1e1e2e !important;
        border: 1px solid #3a3a5a !important;
    }
    li[role="option"] {
        color: #ffffff !important;
    }
    li[role="option"]:hover {
        background: #00adb5 !important;
    }
    
    .result-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 2px solid #00adb5;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: #00adb5 !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.4rem 1rem !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,173,181,0.4);
    }
    
    .top-theme-toggle {
        position: fixed;
        top: 0.8rem;
        right: 1rem;
        z-index: 999;
    }
    .top-theme-toggle button {
        background: rgba(0,173,181,0.15) !important;
        border: 1px solid #00adb5 !important;
        border-radius: 50px !important;
        padding: 0.2rem 0.7rem !important;
        font-size: 0.7rem !important;
        color: white !important;
    }
    
    .profile-card { text-align: center; padding: 0.5rem; }
    .profile-name { font-size: 1rem; font-weight: 700; color: white !important; }
    .profile-role { font-size: 0.65rem; padding: 0.2rem 0.6rem; border-radius: 50px; display: inline-block; background: #00adb520; border: 1px solid #00adb5; color: white !important; }
    
    .stInfo, .stSuccess, .stWarning {
        background-color: rgba(0,173,181,0.2) !important;
        color: #ffffff !important;
    }
    
    hr { margin: 0.8rem 0; border-color: #3a3a5a; }
    input::placeholder { color: #888 !important; }
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
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 2.5rem;">🎓</div>
            <h1 style="font-size: 1.5rem; margin: 0.2rem 0;">Student Score Predictor</h1>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.auth_mode == "login":
            st.markdown('<p style="text-align: center; margin-bottom: 1rem; font-size: 0.8rem;">Sign in to continue</p>', unsafe_allow_html=True)
            
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
            st.markdown(f'<p style="text-align: center; margin-bottom: 0.8rem; font-size: 0.8rem;">Create {role} account</p>', unsafe_allow_html=True)
            
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
                    st.success("Account created!")
                    st.session_state.auth_mode = "login"
                    st.rerun()
            
            st.markdown("<hr>", unsafe_allow_html=True)
            if st.button("← Back to Sign In", use_container_width=True):
                st.session_state.auth_mode = "login"
                st.rerun()
        
        st.markdown('<p style="text-align: center; font-size: 0.55rem; margin-top: 0.8rem;">Secure Portal</p>', unsafe_allow_html=True)

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
            <div style="font-size: 1.8rem;">{role_icon}</div>
            <div class="profile-name">{user_data.get('full_name', st.session_state.username)}</div>
            <div class="profile-role">{role_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Account")
        st.markdown(f"**User:** {st.session_state.username}")
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
    
    st.markdown("<h1 style='text-align: center;'>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)
    
    if st.session_state.user_role == "parent":
        child_name = user_data.get("child_name", "Child")
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
        
        # Save to history
        st.session_state.prediction_history.append(final_score)
        if len(st.session_state.prediction_history) > 10:
            st.session_state.prediction_history = st.session_state.prediction_history[-10:]
        
        # Result Card
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">PREDICTED EXAM SCORE</div>
            <div class="result-score">{final_score}<span style="font-size: 1rem;"> / 100</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        if final_score >= 85:
            st.success("🎉 Exceptional Performance!")
            st.balloons()
        elif final_score >= 70:
            st.success("📈 Good Performance!")
        elif final_score >= 55:
            st.info("📚 Satisfactory")
        else:
            st.warning("⚠️ Needs Improvement")
        
        # =====================================
        # GRAPH - RECOMMENDATIONS SE PEHLE
        # =====================================
        if len(st.session_state.prediction_history) > 1:
            st.markdown("### 📊 Score Trend")
            
            chart_data = pd.DataFrame({
                'Prediction': range(1, len(st.session_state.prediction_history) + 1),
                'Score': st.session_state.prediction_history
            })
            
            st.line_chart(chart_data.set_index('Prediction'), use_container_width=True)
        
        # =====================================
        # RECOMMENDATIONS
        # =====================================
        recs = []
        if hours < 6:
            recs.append("📖 Increase study hours to 6-8 daily")
        if attendance < 75:
            recs.append("📊 Improve attendance to 80%+")
        if sleep < 7:
            recs.append("😴 Get 7-9 hours of sleep")
        if motivation == "Low":
            recs.append("💪 Set daily goals")
        if teacher == "Poor":
            recs.append("👨‍🏫 Seek tutoring")
        if resources == "Low":
            recs.append("📚 Use online resources")
        if peer == "Negative":
            recs.append("🤝 Join positive study groups")
        
        if recs:
            st.markdown("### 💡 Recommendations")
            for r in recs:
                st.info(r)
        else:
            st.success("✅ Excellent habits! Keep going!")
    
    st.markdown("---")
    st.caption("Student Score Predictor | Powered by AI")

# =====================================
# MAIN
# =====================================
if st.session_state.logged_in:
    show_main_app()
else:
    show_auth_page()
