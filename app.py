import streamlit as st
import joblib
import pandas as pd
import numpy as np

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
# SESSION STATE
# =====================================
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# =====================================
# LOAD MODEL
# =====================================
@st.cache_resource
def load_models():
    model = joblib.load("student_model.pkl")
    columns = joblib.load("model_columns.pkl")
    return model, columns

model, columns = load_models()

# =====================================
# LOGIN PAGE CSS
# =====================================
login_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    .login-container {
        background: rgba(18, 18, 30, 0.95);
        border-radius: 20px;
        padding: 3rem;
        max-width: 450px;
        margin: 100px auto;
        text-align: center;
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
    
    .login-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .login-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    
    .login-subtitle {
        color: #888888;
        font-size: 0.85rem;
        margin-bottom: 2rem;
    }
    
    .stButton > button {
        width: 100%;
        background: #00adb5 !important;
        color: white !important;
        border: none;
        border-radius: 50px !important;
        padding: 0.7rem !important;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #007a7f !important;
        transform: translateY(-2px);
    }
    
    .footer {
        margin-top: 2rem;
        color: #555;
        font-size: 0.7rem;
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
    
    .logout-btn {
        position: fixed;
        top: 1rem;
        right: 1rem;
        z-index: 999;
    }
    
    .logout-btn button {
        background: rgba(0, 173, 181, 0.2) !important;
        border: 1px solid #00adb5 !important;
        padding: 0.3rem 1rem !important;
        font-size: 0.8rem !important;
        border-radius: 50px !important;
    }
    
    .logout-btn button:hover {
        background: rgba(0, 173, 181, 0.4) !important;
    }
    
    .stNumberInput label, .stSelectbox label {
        color: #cbd5e0 !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stNumberInput input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 0.5rem 0.8rem !important;
    }
    
    .stNumberInput input:hover {
        border-color: #00adb5 !important;
    }
    
    .stNumberInput button {
        background-color: #2d2d44 !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
    }
    
    .stNumberInput button:hover {
        background-color: #00adb5 !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #1a1a2e !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        min-height: 38px !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #00adb5 !important;
    }
    
    div[data-baseweb="popover"] > div {
        background-color: #1a1a2e !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    
    li[role="option"]:hover {
        background-color: #00adb5 !important;
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
# LOGIN PAGE
# =====================================
def show_login():
    st.markdown(login_css, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="login-container">
        <div class="login-icon">🎓</div>
        <div class="login-title">Student Score Predictor</div>
        <div class="login-subtitle">Predict your exam scores with AI</div>
    """, unsafe_allow_html=True)
    
    if st.button("Continue as Guest", use_container_width=True):
        st.session_state.logged_in = True
        st.rerun()
    
    st.markdown("""
        <div class="footer">
            No registration required • Free to use
        </div>
    </div>
    """, unsafe_allow_html=True)

# =====================================
# MAIN APP
# =====================================
def show_main_app():
    st.markdown(main_css, unsafe_allow_html=True)
    
    # Logout button top right
    st.markdown("""
        <div class="logout-btn">
            <button onclick="location.reload()">Exit</button>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1>Student Score Predictor</h1>", unsafe_allow_html=True)
    
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
    show_login()
