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
# CUSTOM CSS - PURANA WALA BACKGROUND + TEAL BUTTON
# =====================================
st.markdown("""
<style>
/* Main background - Purple Gradient (pehle jaisa) */
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

/* Title - White color (dikhega ab) */
h1 {
    text-align: center;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
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

/* Button - Teal color (tumhare pasand wala) */
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
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
}

.stButton > button:hover {
    background: #007a7f !important;
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(0, 173, 181, 0.4);
}

/* Result Card */
.result-card {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid #00adb5;
    padding: 2rem;
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
    font-size: 3.2rem;
    font-weight: bold;
    margin: 0.5rem 0;
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
}

.result-label {
    color: #888888;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
}

/* Success message */
.stSuccess {
    background-color: rgba(0, 173, 181, 0.1);
    border-left: 3px solid #00adb5;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 1rem;
    color: #00adb5;
}

/* Divider */
hr {
    margin: 1.5rem 0;
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #00adb5, transparent);
}

/* Number input buttons */
.stNumberInput button {
    background-color: #2d2d44 !important;
    border-color: #334155 !important;
    color: white !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #1e1e2e;
}

::-webkit-scrollbar-thumb {
    background: #00adb5;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE - 🎓 CAP KE SAATH
# =====================================
st.markdown("<h1>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)

# =====================================
# TWO COLUMN LAYOUT
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
if st.button("PREDICT SCORE"):
    
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
    
    # Fix score range (40-100)
    final_score = max(40, min(100, prediction[0]))
    final_score = int(round(final_score))
    
    # =====================================
    # OUTPUT RESULT
    # =====================================
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">PREDICTED SCORE</div>
        <div class="result-score">{final_score}/100</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simple success message
    if final_score >= 80:
        st.success(f"🎯 Exam Score: {final_score}")
        st.balloons()
    else:
        st.success(f"🎯 Exam Score: {final_score}")
