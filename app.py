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
# CUSTOM CSS - DARK THEME WITH BLACK TITLE
# =====================================
st.markdown("""
<style>
/* Main background - Dark */
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
}

/* Title - Black color, Cap bhi black */
h1 {
    text-align: center;
    font-size: 2.3rem !important;
    font-weight: 700 !important;
    color: #000000 !important;
    margin-bottom: 2rem;
    font-family: 'Segoe UI', 'Helvetica Neue', sans-serif;
    background: none !important;
    -webkit-text-fill-color: #000000 !important;
}

/* Labels */
.stNumberInput label, .stSelectbox label {
    color: #cccccc !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    margin-bottom: 0.3rem !important;
}

/* Input fields */
.stNumberInput input {
    background-color: #1a1a1a !important;
    color: white !important;
    border: 1px solid #333333 !important;
    border-radius: 6px !important;
    padding: 0.5rem !important;
}

.stNumberInput input:focus {
    border-color: #555555 !important;
    outline: none !important;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    background-color: #1a1a1a !important;
    border: 1px solid #333333 !important;
    border-radius: 6px !important;
}

div[data-baseweb="select"] input {
    color: white !important;
}

/* Dropdown */
div[data-baseweb="popover"] div {
    background-color: #1a1a1a !important;
    border: 1px solid #333333 !important;
}

li[role="option"] {
    color: white !important;
    background-color: #1a1a1a !important;
}

li[role="option"]:hover {
    background-color: #2a2a2a !important;
}

/* Button - New Color (Teal/Green) */
.stButton > button {
    width: 100%;
    height: 52px;
    border: none;
    border-radius: 8px;
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
    box-shadow: 0 5px 15px rgba(0, 173, 181, 0.3);
}

/* Result Card */
.result-card {
    background: #1a1a1a;
    border: 1px solid #00adb5;
    padding: 2rem;
    border-radius: 12px;
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
}

.result-label {
    color: #888888;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Success message */
.stSuccess {
    background-color: rgba(0, 173, 181, 0.1);
    border-left: 3px solid #00adb5;
    border-radius: 6px;
    padding: 1rem;
    margin-top: 1rem;
    color: #00adb5;
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
    color: white !important;
}

/* Remove default blue outline */
input:focus, select:focus, textarea:focus {
    outline: none !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE - BLACK COLOR
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
