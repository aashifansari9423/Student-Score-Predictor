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
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================
# LOAD MODEL
# =====================================
model = joblib.load("student_model.pkl")
columns = joblib.load("model_columns.pkl")

# =====================================
# CUSTOM CSS - MOBILE + LAPTOP FIX
# =====================================
st.markdown("""
<style>
    /* Force all text white on ALL devices */
    * {
        color: #ffffff !important;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    /* Main container */
    .main .block-container {
        background: rgba(18, 18, 30, 0.92);
        border-radius: 16px;
        padding: 1.5rem;
    }
    
    /* Title */
    h1 {
        text-align: center;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin-bottom: 1.8rem;
    }
    
    /* Labels */
    .stNumberInput label, .stSelectbox label {
        color: #cbd5e0 !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        margin-bottom: 0.2rem !important;
    }
    
    /* Input fields */
    .stNumberInput input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #2d2d44 !important;
        border-radius: 10px !important;
        padding: 0.5rem 0.8rem !important;
    }
    
    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #1a1a2e !important;
        border: 1px solid #2d2d44 !important;
        border-radius: 10px !important;
        min-height: 38px !important;
    }
    
    div[data-baseweb="select"] input {
        color: #ffffff !important;
        background: transparent !important;
    }
    
    /* Dropdown */
    div[data-baseweb="popover"] > div {
        background-color: #1a1a2e !important;
        border: 1px solid #2d2d44 !important;
        border-radius: 10px !important;
    }
    
    li[role="option"] {
        color: #ffffff !important;
        background-color: #1a1a2e !important;
    }
    
    li[role="option"]:hover {
        background-color: #00adb5 !important;
    }
    
    /* Button */
    .stButton > button {
        width: 100%;
        height: 52px;
        background: #00adb5 !important;
        color: #ffffff !important;
        border: none;
        border-radius: 50px !important;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #007a7f !important;
        transform: translateY(-2px);
    }
    
    /* Result Card */
    .result-card {
        background: #1a1a2e;
        border: 2px solid #00adb5;
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        margin-top: 1.5rem;
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
        color: #aaaaaa !important;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .result-score {
        color: #00adb5 !important;
        font-size: 2.8rem;
        font-weight: 800;
    }
    
    /* Success message */
    .stSuccess {
        background-color: rgba(0, 173, 181, 0.1);
        border-left: 3px solid #00adb5;
        border-radius: 12px;
        padding: 0.8rem;
        margin-top: 1rem;
    }
    
    /* Fix columns - SAME HEIGHT on laptop & mobile */
    div[data-testid="column"] {
        padding: 0 0.8rem;
    }
    
    /* Mobile specific */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        /* Force columns to stay side by side on mobile */
        div[data-testid="column"] {
            padding: 0 0.3rem;
        }
        
        .stNumberInput input, div[data-baseweb="select"] > div {
            min-height: 42px;
        }
        
        .stButton > button {
            height: 48px;
            font-size: 0.9rem;
        }
        
        .result-score {
            font-size: 2rem;
        }
    }
    
    /* Remove any default Streamlit blue */
    .st-bw, .st-bx {
        background-color: transparent !important;
    }
    
    /* Fix number input buttons */
    .stNumberInput button {
        background-color: #2d2d44 !important;
        border-color: #2d2d44 !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.markdown("<h1>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)

# =====================================
# TWO COLUMNS - SIDE BY SIDE ON ALL DEVICES
# =====================================
col1, col2 = st.columns(2, gap="medium")

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

# =====================================
# PREDICT BUTTON
# =====================================
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
    
    # Result Card
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">PREDICTED EXAM SCORE</div>
        <div class="result-score">{final_score}<span style="font-size: 1rem;">/100</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Success message
    if final_score >= 80:
        st.success(f"🎉 Predicted Exam Score: {final_score}")
        st.balloons()
    else:
        st.success(f"📌 Predicted Exam Score: {final_score}")
