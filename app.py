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
    /* Main Background */
    .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .main .block-container { background: rgba(255, 255, 255, 0.95); border-radius: 20px; padding: 1.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
    [data-testid="stSidebar"] { background: rgba(255, 255, 255, 0.95); border-right: 1px solid #e0e0e0; }
    
    /* Text Colors */
    h1, h2, h3, p, label, .stMarkdown, .stCaption { color: #1a1a2e !important; }
    
    /* Input Fields - Full Hover */
    .stNumberInput input, div[data-baseweb="select"] > div, .stTextInput input {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
        border: 1px solid #ddd !important;
        border-radius: 10px !important;
        padding: 0.4rem 0.8rem !important;
        transition: all 0.3s ease !important;
    }
    .stNumberInput input:hover, div[data-baseweb="select"] > div:hover, .stTextInput input:hover {
        border-color: #667eea !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102,126,234,0.15);
    }
    .stNumberInput input:focus, div[data-baseweb="select"] > div:focus, .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102,126,234,0.2);
    }
    
    /* Number Buttons - Full Hover */
    .stNumberInput button {
        background-color: #f0f0f0 !important;
        border: 1px solid #ddd !important;
        transition: all 0.3s ease !important;
        border-radius: 6px !important;
    }
    .stNumberInput button:hover {
        background-color: #667eea !important;
        color: white !important;
        transform: scale(1.05);
    }
    
    /* Select Dropdown - Text FULL Visible */
    div[data-baseweb="select"] input {
        color: #1a1a2e !important;
        -webkit-text-fill-color: #1a1a2e !important;
        font-size: 0.85rem !important;
    }
    div[data-baseweb="select"] [data-testid="stMarkdownContainer"] p {
        color: #1a1a2e !important;
    }
    
    /* Dropdown Menu Items */
    div[data-baseweb="popover"] div {
        background-color: #ffffff !important;
        border: 1px solid #ddd !important;
        border-radius: 10px !important;
    }
    li[role="option"] {
        color: #1a1a2e !important;
        transition: all 0.2s ease;
        padding: 8px 12px !important;
    }
    li[role="option"]:hover {
        background-color: #667eea !important;
        color: white !important;
        transform: translateX(5px);
    }
    
    /* Result Card */
    .result-card { background: #ffffff; border: 2px solid #667eea; border-radius: 20px; padding: 1.2rem; text-align: center; margin: 1rem 0; transition: all 0.3s ease; }
    .result-card:hover { transform: scale(1.02); box-shadow: 0 10px 30px rgba(102,126,234,0.2); }
    .result-score { color: #667eea !important; font-size: 2.2rem; font-weight: 800; }
    .result-label { color: #888 !important; font-size: 0.7rem; letter-spacing: 1px; }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.4rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102,126,234,0.4);
    }
    
    hr { margin: 0.8rem 0; border-color: #e0e0e0; }
    input::placeholder { color: #aaa !important; font-size: 0.8rem; }
    
    /* Sidebar */
    .profile-card { text-align: center; padding: 0.5rem; }
    .profile-name { font-size: 1rem; font-weight: 700; }
    .profile-role { font-size: 0.65rem; padding: 0.2rem 0.6rem; border-radius: 50px; display: inline-block; }
    
    /* Theme Toggle - RIGHT SIDE */
    .top-theme-toggle {
        position: fixed;
        top: 0.8rem;
        right: 1rem;
        z-index: 999;
    }
    .top-theme-toggle button {
        background: rgba(102,126,234,0.15) !important;
        border: 1px solid #667eea !important;
        border-radius: 50px !important;
        padding: 0.25rem 0.8rem !important;
        font-size: 0.7rem !important;
        font-weight: 500 !important;
    }
    .top-theme-toggle button:hover {
        background: rgba(102,126,234,0.3) !important;
        transform: translateY(-2px);
    }
</style>
"""

dark_theme_css = """
<style>
    /* Main Background */
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); }
    .main .block-container { background: rgba(18, 18, 30, 0.92); border-radius: 20px; padding: 1.5rem; border: 1px solid #2a2a4a; }
    [data-testid="stSidebar"] { background: rgba(18, 18, 30, 0.95); border-right: 1px solid #2a2a4a; }
    
    /* Text Colors */
    h1, h2, h3, p, label, .stMarkdown, .stCaption { color: #ffffff !important; }
    
    /* Input Fields - Full Hover */
    .stNumberInput input, div[data-baseweb="select"] > div, .stTextInput input {
        background-color: #1e1e2e !important;
        color: #ffffff !important;
        border: 1px solid #3a3a5a !important;
        border-radius: 10px !important;
        padding: 0.4rem 0.8rem !important;
        transition: all 0.3s ease !important;
    }
    .stNumberInput input:hover, div[data-baseweb="select"] > div:hover, .stTextInput input:hover {
        border-color: #00adb5 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,173,181,0.2);
    }
    .stNumberInput input:focus, div[data-baseweb="select"] > div:focus, .stTextInput input:focus {
        border-color: #00adb5 !important;
        box-shadow: 0 0 0 2px rgba(0,173,181,0.2);
    }
    
    /* Number Buttons - Full Hover */
    .stNumberInput button {
        background-color: #2d2d44 !important;
        border: 1px solid #3a3a5a !important;
        transition: all 0.3s ease !important;
        border-radius: 6px !important;
    }
    .stNumberInput button:hover {
        background-color: #00adb5 !important;
        transform: scale(1.05);
    }
    
    /* Select Dropdown - Text FULL Visible */
    div[data-baseweb="select"] input {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-size: 0.85rem !important;
    }
    div[data-baseweb="select"] [data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }
    
    /* Dropdown Menu Items */
    div[data-baseweb="popover"] div {
        background-color: #1e1e2e !important;
        border: 1px solid #3a3a5a !important;
        border-radius: 10px !important;
    }
    li[role="option"] {
        color: #ffffff !important;
        transition: all 0.2s ease;
        padding: 8px 12px !important;
    }
    li[role="option"]:hover {
        background-color: #00adb5 !important;
        transform: translateX(5px);
    }
    
    /* Result Card */
    .result-card { background: #1e1e2e; border: 2px solid #00adb5; border-radius: 20px; padding: 1.2rem; text-align: center; margin: 1rem 0; transition: all 0.3s ease; }
    .result-card:hover { transform: scale(1.02); box-shadow: 0 10px 30px rgba(0,173,181,0.2); }
    .result-score { color: #00adb5 !important; font-size: 2.2rem; font-weight: 800; }
    .result-label { color: #888 !important; font-size: 0.7rem; letter-spacing: 1px; }
    
    /* Buttons */
    .stButton > button {
        background: #00adb5 !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.4rem 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,173,181,0.4);
    }
    
    hr { margin: 0.8rem 0; border-color: #3a3a5a; }
    input::placeholder { color: #888 !important; font-size: 0.8rem; }
    
    /* Sidebar */
    .profile-card { text-align: center; padding: 0.5rem; }
    .profile-name { font-size: 1rem; font-weight: 700; }
    .profile-role { font-size: 0.65rem; padding: 0.2rem 0.6rem; border-radius: 50px; display: inline-block; }
    
    /* Theme Toggle - RIGHT SIDE */
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
        padding: 0.25rem 0.8rem !important;
        font-size: 0.7rem !important;
        font-weight: 500 !important;
    }
    .top-theme-toggle button:hover {
        background: rgba(0,173,181,0.3) !important;
        transform: translateY(-2px);
    }
</style>
"""

def apply_theme():
    if st.session_state.theme == "dark":
        st.markdown(dark_theme_css, unsafe_allow_html=True)
    else:
        st.markdown(light_theme_css, unsafe_allow_html=True)

# =====================================
# AUTH PAGE
# =====================================
def show_auth_page():
    apply_theme()
    
    # Theme Toggle - RIGHT SIDE
    st.markdown('<div class="top-theme-toggle">', unsafe_allow_html=True)
    mode_text = "Light" if st.session_state.theme == "dark" else "Dark"
    mode_icon = "☀️" if st.session_state.theme == "dark" else "🌙"
    if st.button(f"{mode_icon} {mode_text}", key="theme_toggle_auth"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    users = load_users()
    
    # CENTER BOX
    col1, col2, col3 = st.columns([1, 2.5, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="font-size: 3rem;">🎓</div>
            <h1 style="font-size: 1.8rem; margin: 0;">Student Score Predictor</h1>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.auth_mode == "login":
            st.markdown('<p style="text-align: center; color: #888; margin-bottom: 1.5rem;">Welcome back! Please sign in</p>', unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
            
            if username and username in users:
                role = users[username]["role"]
                role_icon = "👨‍🎓" if role == "student" else "👨‍👩‍👧"
                role_text = "Student" if role == "student" else "Parent"
                st.markdown(f'<p style="text-align: center; font-size: 0.75rem; margin-top: -0.5rem;"><span style="background: rgba(0,173,181,0.15); padding: 0.2rem 0.8rem; border-radius: 20px;">{role_icon} Login as {role_text}</span></p>', unsafe_allow_html=True)
            
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
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📝 Student Sign Up", use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.session_state.signup_role = "student"
                    st.rerun()
            with col_b:
                if st.button("👨‍👩‍👧 Parent Sign Up", use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.session_state.signup_role = "parent"
                    st.rerun()
        
        else:
            role = st.session_state.signup_role
            st.markdown(f'<p style="text-align: center; color: #888; margin-bottom: 1.5rem;">Create {role} account</p>', unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("👨‍🎓 Student", use_container_width=True):
                    st.session_state.signup_role = "student"
                    st.rerun()
            with col_b:
                if st.button("👨‍👩‍👧 Parent", use_container_width=True):
                    st.session_state.signup_role = "parent"
                    st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            username = st.text_input("Username", placeholder="Choose username", key="signup_username")
            password = st.text_input("Password", type="password", placeholder="Choose password", key="signup_password")
            confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm password", key="signup_confirm")
            full_name = st.text_input("Full Name", placeholder="Enter full name", key="signup_name")
            
            if role == "student":
                dob = st.date_input("Date of Birth", min_value=datetime(1990,1,1), max_value=datetime.now())
                grade = st.selectbox("Grade", ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12", "College"])
                school = st.text_input("School Name", placeholder="Enter school name")
            else:
                child_name = st.text_input("Child's Name", placeholder="Enter child's name")
                child_dob = st.date_input("Child's Date of Birth", min_value=datetime(1990,1,1), max_value=datetime.now())
                child_grade = st.selectbox("Child's Grade", ["Class 8", "Class 9", "Class 10", "Class 11", "Class 12", "College"])
                relation = st.selectbox("Relationship", ["Father", "Mother", "Guardian"])
            
            if st.button("Create Account", use_container_width=True):
                if not username or not password or not full_name:
                    st.warning("Please fill all fields")
                elif password != confirm:
                    st.error("Passwords do not match")
                elif len(password) < 4:
                    st.warning("Password must be at least 4 characters")
                elif username in users:
                    st.error("Username already exists")
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
        
        st.markdown('<p style="text-align: center; font-size: 0.65rem; color: #888; margin-top: 1rem;">Secure • Student & Parent Portals</p>', unsafe_allow_html=True)

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
        role_icon = "👨‍🎓" if st.session_state.user_role == "student" else "👨‍👩‍👧"
        
        st.markdown(f"""
        <div class="profile-card">
            <div style="font-size: 2rem;">{role_icon}</div>
            <div class="profile-name">{user_data.get('full_name', st.session_state.username)}</div>
            <div class="profile-role" style="background: {'#667eea' if st.session_state.theme == 'light' else '#00adb5'}20; border: 1px solid {'#667eea' if st.session_state.theme == 'light' else '#00adb5'};">{role_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Profile Details")
        st.markdown(f"**Username:** {st.session_state.username}")
        
        if st.session_state.user_role == "student":
            st.markdown(f"**Full Name:** {user_data.get('full_name', 'N/A')}")
            st.markdown(f"**Age:** {user_data.get('age', 'N/A')}")
            st.markdown(f"**Grade:** {user_data.get('grade', 'N/A')}")
            st.markdown(f"**School:** {user_data.get('school', 'N/A')}")
        else:
            st.markdown(f"**Parent Name:** {user_data.get('full_name', 'N/A')}")
            st.markdown(f"**Relationship:** {user_data.get('relation', 'N/A')}")
            st.markdown(f"**Child Name:** {user_data.get('child_name', 'N/A')}")
            st.markdown(f"**Child Age:** {user_data.get('child_age', 'N/A')}")
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
    
    # Theme Toggle - RIGHT SIDE
    st.markdown('<div class="top-theme-toggle">', unsafe_allow_html=True)
    mode_text = "Light" if st.session_state.theme == "dark" else "Dark"
    mode_icon = "☀️" if st.session_state.theme == "dark" else "🌙"
    if st.button(f"{mode_icon} {mode_text}", key="theme_toggle_main"):
        st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    users = load_users()
    user_data = users.get(st.session_state.username, {})
    
    show_sidebar(user_data)
    
    st.markdown("<h1 style='text-align: center;'>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)
    
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
    
    if st.button("🔮 Predict Score", use_container_width=True):
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
            <div class="result-score">{final_score}<span style="font-size: 1rem;"> / 100</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        if final_score >= 85:
            st.success("🎉 Exceptional Performance!")
            st.balloons()
        elif final_score >= 70:
            st.success("📈 Good Performance!")
        elif final_score >= 55:
            st.info("📚 Satisfactory Performance")
        else:
            st.warning("⚠️ Needs Improvement")
        
        recommendations = []
        if hours < 6: recommendations.append("📖 Increase study hours to 6-8 hours daily")
        if attendance < 75: recommendations.append("📊 Improve attendance to 80% or higher")
        if sleep < 7: recommendations.append("😴 Get 7-9 hours of sleep for better focus")
        if motivation == "Low": recommendations.append("💪 Set daily goals to boost motivation")
        if teacher == "Poor": recommendations.append("👨‍🏫 Seek additional tutoring or online resources")
        if resources == "Low": recommendations.append("📚 Utilize free online learning materials")
        if peer == "Negative": recommendations.append("🤝 Join positive study groups")
        
        if recommendations:
            st.markdown("### 💡 Recommendations")
            for rec in recommendations:
                st.info(rec)
        else:
            st.success("✅ Excellent study habits! Keep it up!")
    
    st.markdown("---")
    st.caption("Student Score Predictor | AI-Powered Academic Tool")

# =====================================
# MAIN ROUTER
# =====================================
if st.session_state.logged_in:
    show_main_app()
else:
    show_auth_page()
