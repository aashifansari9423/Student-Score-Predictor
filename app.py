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
# CUSTOM CSS - DARK THEME + TEAL BUTTON
# =====================================
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}

/* Main container */
.main .block-container {
    background: rgba(18, 18, 30, 0.92);
    border-radius: 15px;
    padding: 2rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Title */
h1 {
    text-align: center;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    color: white !important;
    margin-bottom: 2rem;
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
}

/* Labels */
.stNumberInput label, .stSelectbox label {
    color: #e2e8f0 !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    margin-bottom: 0.3rem !important;
}

/* Input fields */
.stNumberInput input {
    background-color: #1e1e2e !important;
    color: white !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    padding: 0.5rem !important;
}

.stNumberInput input:focus {
    border-color: #00adb5 !important;
    box-shadow: 0 0 0 1px rgba(0, 173, 181, 0.3) !important;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    background-color: #1e1e2e !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"] input {
    color: white !important;
}

/* Dropdown */
div[data-baseweb="popover"] div {
    background-color: #1e1e2e !important;
    border: 1px solid #334155 !important;
}

li[role="option"] {
    color: white !important;
    background-color: #1e1e2e !important;
}

li[role="option"]:hover {
    background-color: #2d2d44 !important;
}

/* Button - Teal color */
.stButton > button {
    width: 100%;
    height: 52px;
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

/* Success message */
.stSuccess {
    background-color: rgba(0, 173, 181, 0.1);
    border-left: 3px solid #00adb5;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 1rem;
    color: #00adb5;
    font-size: 1.1rem;
    font-weight: 500;
}

/* Number input buttons */
.stNumberInput button {
    background-color: #2d2d44 !important;
    border-color: #334155 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.title("🎓 Student Score Predictor")

# =====================================
# INPUT FIELDS - VERTICAL LAYOUT (JAISA PEHLE THA)
# =====================================
hours = st.number_input("Hours Studied", 0.0, 24.0, step=0.5)
attendance = st.number_input("Attendance", 0.0, 100.0, step=5.0)
previous = st.number_input("Previous Score", 0.0, 100.0, step=5.0)
sleep = st.number_input("Sleep Hours", 0.0, 12.0, step=0.5)

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
# PREDICTION BUTTON
# =====================================
if st.button("Predict Score"):

    # Create input dictionary
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

    # Convert to DataFrame
    input_df = pd.DataFrame([data])

    # Apply encoding
    input_df = pd.get_dummies(input_df)

    # Match training columns
    input_df = input_df.reindex(columns=columns, fill_value=0)

    # =========================
    # PREDICT
    # =========================
    prediction = model.predict(input_df)

    # =========================
    # FIX UNREALISTIC VALUES
    # =========================
    final_score = max(40, min(100, prediction[0]))

    # Convert to integer
    final_score = int(round(final_score))

    # =========================
    # OUTPUT
    # =========================
    st.success(f"🎯 Predicted Exam Score: {final_score}")
    
    # Balloons for high score
    if final_score >= 85:
        st.balloons()
