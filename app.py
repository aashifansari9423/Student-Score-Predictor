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
    layout="centered"
)

# =====================================
# LOAD MODEL
# =====================================
model = joblib.load("student_model.pkl")
columns = joblib.load("model_columns.pkl")

# =====================================
# SIMPLE CSS - NORMAL STYLING
# =====================================
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: #0a0a0a;
    }
    
    /* Container */
    .main .block-container {
        background: #111111;
        border-radius: 12px;
        padding: 2rem;
    }
    
    /* Title */
    h1 {
        text-align: center;
        color: white !important;
        margin-bottom: 2rem;
    }
    
    /* Labels */
    .stNumberInput label, .stSelectbox label {
        color: white !important;
        font-weight: 500;
    }
    
    /* Inputs */
    .stNumberInput input {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
    }
    
    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
    }
    
    div[data-baseweb="select"] input {
        color: white !important;
    }
    
    /* Dropdown */
    div[data-baseweb="popover"] div {
        background-color: #1a1a1a !important;
        border: 1px solid #333 !important;
    }
    
    li[role="option"] {
        color: white !important;
        background-color: #1a1a1a !important;
    }
    
    li[role="option"]:hover {
        background-color: #333 !important;
    }
    
    /* Button */
    .stButton > button {
        width: 100%;
        background: #00adb5 !important;
        color: white !important;
        border: none;
        border-radius: 8px !important;
        padding: 0.6rem;
        font-weight: bold;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        background: #007a7f !important;
    }
    
    /* Success message */
    .stSuccess {
        background-color: #1a3a3a;
        border-left-color: #00adb5;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.title("🎓 Student Score Predictor")

# =====================================
# INPUTS - NORMAL SIMPLE
# =====================================
hours = st.number_input("Hours Studied", min_value=0.0, max_value=24.0, value=5.0, step=0.5)
attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=75.0, step=5.0)
previous = st.number_input("Previous Score", min_value=0.0, max_value=100.0, value=60.0, step=5.0)
sleep = st.number_input("Sleep Hours", min_value=0.0, max_value=12.0, value=7.0, step=0.5)

motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
teacher = st.selectbox("Teacher Quality", ["Poor", "Average", "Good"])
school = st.selectbox("School Type", ["Public", "Private"])
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
if st.button("PREDICT SCORE"):
    
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
    
    # Output
    st.success(f"Predicted Exam Score: {final_score}")
    
    if final_score >= 80:
        st.balloons()
