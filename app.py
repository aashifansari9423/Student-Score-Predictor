import streamlit as st
import joblib
import pandas as pd
import numpy as np

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="📊",
    layout="centered"
)

# =====================================
# LOAD MODEL
# =====================================
try:
    model = joblib.load("student_model.pkl")
    columns = joblib.load("model_columns.pkl")
except:
    st.error("Model files not found. Please ensure 'student_model.pkl' and 'model_columns.pkl' exist.")
    st.stop()

# =====================================
# PROFESSIONAL DARK THEME CSS
# =====================================
st.markdown("""
<style>
    /* Main dark background */
    .stApp {
        background: #0a0a0a;
    }
    
    /* Main container */
    .main .block-container {
        background: #111111;
        border-radius: 12px;
        padding: 2rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #222222;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    /* Title - Clean, no gradient, just white */
    h1 {
        text-align: center;
        font-size: 2.2rem !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        margin-bottom: 2rem;
        letter-spacing: -0.5px;
        border-bottom: 2px solid #2c2c2c;
        padding-bottom: 1rem;
    }
    
    /* Labels */
    .stNumberInput label, .stSelectbox label {
        color: #cccccc !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.3rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Input fields */
    .stNumberInput input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
        padding: 0.6rem !important;
        font-size: 0.9rem !important;
    }
    
    .stNumberInput input:focus {
        border-color: #555555 !important;
        box-shadow: 0 0 0 1px #555555 !important;
    }
    
    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important;
        border: 1px solid #333333 !important;
        border-radius: 6px !important;
    }
    
    div[data-baseweb="select"] input {
        color: #ffffff !important;
        font-size: 0.9rem !important;
    }
    
    /* Dropdown menu */
    div[data-baseweb="popover"] div {
        background-color: #1a1a1a !important;
        border: 1px solid #333333 !important;
    }
    
    li[role="option"] {
        color: #ffffff !important;
        background-color: #1a1a1a !important;
    }
    
    li[role="option"]:hover {
        background-color: #2a2a2a !important;
    }
    
    /* Button */
    .stButton > button {
        width: 100%;
        height: 48px;
        border: none;
        border-radius: 6px;
        background: #222222;
        color: #ffffff;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.2s ease;
        margin-top: 1.5rem;
        cursor: pointer;
        border: 1px solid #333333;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        background: #2a2a2a;
        border-color: #555555;
    }
    
    /* Result Card - Sleek */
    .result-card {
        background: #0d0d0d;
        border: 1px solid #222222;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        animation: fadeIn 0.4s ease-out;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-title {
        color: #999999;
        font-size: 0.85rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
    }
    
    .result-score {
        color: #ffffff;
        font-size: 3.5rem;
        font-weight: 600;
        letter-spacing: -1px;
    }
    
    .score-unit {
        font-size: 1rem;
        color: #666666;
        margin-left: 5px;
    }
    
    /* Message boxes - Professional */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 6px;
        padding: 1rem;
        margin-top: 1rem;
        border-left: 3px solid;
    }
    
    .stSuccess {
        background-color: #0a1a0a;
        border-left-color: #2e7d32;
    }
    
    .stInfo {
        background-color: #0a1a2a;
        border-left-color: #1565c0;
    }
    
    .stWarning {
        background-color: #1a1a0a;
        border-left-color: #f57c00;
    }
    
    .stError {
        background-color: #1a0a0a;
        border-left-color: #c62828;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: #222222;
    }
    
    /* Number input buttons */
    .stNumberInput button {
        background-color: #1a1a1a !important;
        border-color: #333333 !important;
        color: #ffffff !important;
    }
    
    /* Hint text */
    .stNumberInput div[data-testid="stMarkdownContainer"] small {
        color: #666666 !important;
    }
    
    /* Remove default streamlit padding issues */
    div[data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #111111;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #333333;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #444444;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.markdown("<h1>STUDENT SCORE PREDICTOR</h1>", unsafe_allow_html=True)

# =====================================
# TWO COLUMN LAYOUT
# =====================================
col1, col2 = st.columns(2)

with col1:
    hours = st.number_input(
        "HOURS STUDIED",
        min_value=0.0,
        max_value=24.0,
        value=5.0,
        step=0.5,
        help="Daily study hours"
    )
    
    attendance = st.number_input(
        "ATTENDANCE (%)",
        min_value=0.0,
        max_value=100.0,
        value=75.0,
        step=5.0,
        help="Attendance percentage"
    )
    
    previous = st.number_input(
        "PREVIOUS SCORE",
        min_value=0.0,
        max_value=100.0,
        value=60.0,
        step=5.0,
        help="Previous exam score"
    )
    
    sleep = st.number_input(
        "SLEEP HOURS",
        min_value=0.0,
        max_value=12.0,
        value=7.0,
        step=0.5,
        help="Average daily sleep"
    )
    
    motivation = st.selectbox(
        "MOTIVATION LEVEL",
        ["Low", "Medium", "High"]
    )
    
    teacher = st.selectbox(
        "TEACHER QUALITY",
        ["Poor", "Average", "Good"]
    )
    
    school = st.selectbox(
        "SCHOOL TYPE",
        ["Public", "Private"]
    )

with col2:
    internet = st.selectbox(
        "INTERNET ACCESS",
        ["Yes", "No"]
    )
    
    income = st.selectbox(
        "FAMILY INCOME",
        ["Low", "Medium", "High"]
    )
    
    parent = st.selectbox(
        "PARENTAL INVOLVEMENT",
        ["Low", "Medium", "High"]
    )
    
    education = st.selectbox(
        "PARENT EDUCATION",
        ["School", "College"]
    )
    
    peer = st.selectbox(
        "PEER INFLUENCE",
        ["Negative", "Neutral", "Positive"]
    )
    
    resources = st.selectbox(
        "LEARNING RESOURCES",
        ["Low", "Medium", "High"]
    )
    
    activities = st.selectbox(
        "EXTRACURRICULAR ACTIVITIES",
        ["Yes", "No"]
    )

# =====================================
# PREDICT BUTTON
# =====================================
if st.button("PREDICT SCORE", use_container_width=True):
    
    # Input Data
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
    
    # Create DataFrame
    input_df = pd.DataFrame([data])
    
    # One-hot encoding
    input_df = pd.get_dummies(input_df)
    
    # Align with training columns
    input_df = input_df.reindex(columns=columns, fill_value=0)
    
    # Make prediction
    try:
        prediction = model.predict(input_df)
        
        # Clamp prediction between 0-100
        final_score = int(round(np.clip(prediction[0], 0, 100)))
        
        # Result Card
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">PREDICTED SCORE</div>
            <div class="result-score">{final_score}<span class="score-unit">/100</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Performance Assessment
        if final_score >= 85:
            st.success("EXCEPTIONAL PERFORMANCE")
            st.info("Maintain current study patterns for consistent results.")
            
        elif final_score >= 70:
            st.info("GOOD PERFORMANCE")
            st.info("Consider increasing study hours to achieve higher scores.")
            
        elif final_score >= 50:
            st.warning("SATISFACTORY PERFORMANCE")
            st.warning("Room for improvement exists. Review study habits and attendance.")
            
        else:
            st.error("NEEDS IMPROVEMENT")
            st.markdown("""
            **Recommendations:**
            - Increase daily study hours (target: 6-8 hours)
            - Improve attendance (target: >80%)
            - Ensure adequate sleep (7-9 hours)
            - Set specific academic goals
            """)
            
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        st.info("Please verify all inputs and try again.")
