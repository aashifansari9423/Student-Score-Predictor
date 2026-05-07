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
# LOAD MODEL
# =====================================
model = joblib.load("student_model.pkl")
columns = joblib.load("model_columns.pkl")

# =====================================
# CUSTOM CSS - FIXED FOR MOBILE & CLEAN DROPDOWNS
# =====================================
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    /* Main container - better padding for mobile */
    .main .block-container {
        background: rgba(18, 18, 30, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Title - white for mobile too */
    h1 {
        text-align: center;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        margin-bottom: 1.5rem;
        font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
    }
    
    /* Labels - always white */
    .stNumberInput label, .stSelectbox label {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.3rem !important;
    }
    
    /* Input fields */
    .stNumberInput input {
        background-color: #1e1e2e !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 0.6rem !important;
        font-size: 0.9rem !important;
    }
    
    /* Remove inner box from dropdown - CLEAN */
    div[data-baseweb="select"] {
        margin-top: 0 !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: #1e1e2e !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        min-height: 38px !important;
        box-shadow: none !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #00adb5 !important;
    }
    
    div[data-baseweb="select"] input {
        color: #ffffff !important;
        font-size: 0.9rem !important;
        background: transparent !important;
        border: none !important;
    }
    
    /* Dropdown menu - clean */
    div[data-baseweb="popover"] {
        border-radius: 8px !important;
        overflow: hidden !important;
    }
    
    div[data-baseweb="popover"] div {
        background-color: #1e1e2e !important;
        border: 1px solid #334155 !important;
    }
    
    li[role="option"] {
        color: #ffffff !important;
        background-color: #1e1e2e !important;
        padding: 10px 12px !important;
        font-size: 0.9rem !important;
    }
    
    li[role="option"]:hover {
        background-color: #00adb5 !important;
        color: white !important;
    }
    
    li[role="option"][aria-selected="true"] {
        background-color: #00adb5 !important;
        color: white !important;
    }
    
    /* Button */
    .stButton > button {
        width: 100%;
        height: 50px;
        border: none;
        border-radius: 10px;
        background: #00adb5 !important;
        color: white;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-top: 1rem;
        cursor: pointer;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: #007a7f !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0, 173, 181, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Result Card */
    .result-card {
        background: #1a1a2e;
        border: 1px solid #00adb5;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-top: 1.5rem;
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-score {
        color: #00adb5;
        font-size: 3rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .result-label {
        color: #888888;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Success message */
    .stSuccess {
        background-color: rgba(0, 173, 181, 0.15);
        border-left: 3px solid #00adb5;
        border-radius: 8px;
        padding: 0.8rem;
        margin-top: 1rem;
        color: #00adb5 !important;
    }
    
    /* Divider */
    hr {
        margin: 1rem 0;
        border: none;
        height: 1px;
        background: #334155;
    }
    
    /* Number input buttons - mobile friendly */
    .stNumberInput button {
        background-color: #2d2d44 !important;
        border-color: #334155 !important;
        color: white !important;
    }
    
    /* Remove extra spacing for mobile */
    div[data-testid="column"] {
        padding: 0 0.3rem !important;
    }
    
    /* Mobile specific fixes */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem !important;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        .stNumberInput input, div[data-baseweb="select"] > div {
            min-height: 44px !important;
            font-size: 1rem !important;
        }
        
        .stButton > button {
            height: 48px;
            font-size: 0.9rem;
        }
        
        .result-score {
            font-size: 2.2rem;
        }
    }
    
    /* Force white text everywhere on mobile */
    * {
        -webkit-text-fill-color: initial;
    }
    
    input, select, textarea, div {
        color: #ffffff !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e1e2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00adb5;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.markdown("<h1>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)

# =====================================
# TWO COLUMN LAYOUT - CLEAN
# =====================================
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

# =====================================
# PREDICT BUTTON
# =====================================
if st.button("PREDICT SCORE", use_container_width=True):
    
    # Input data
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
    
    # DataFrame
    input_df = pd.DataFrame([data])
    
    # Encoding
    input_df = pd.get_dummies(input_df)
    
    # Match columns
    input_df = input_df.reindex(columns=columns, fill_value=0)
    
    # Prediction
    prediction = model.predict(input_df)
    
    # Fix score range
    final_score = max(40, min(100, prediction[0]))
    final_score = int(round(final_score))
    
    # Output Result
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">PREDICTED SCORE</div>
        <div class="result-score">{final_score}/100</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Success message
    if final_score >= 80:
        st.success(f"🎯 Exam Score: {final_score}")
        st.balloons()
    else:
        st.success(f"🎯 Exam Score: {final_score}")
