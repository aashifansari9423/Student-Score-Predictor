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
# CUSTOM CSS
# =====================================
st.markdown("""
<style>

    /* All Text White */
    .stApp, .stApp * {
        color: #ffffff !important;
    }

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }

    /* Remove Focus Outline */
    *:focus {
        outline: none !important;
        box-shadow: none !important;
    }

    /* Main Container */
    .main .block-container {
        background: rgba(18, 18, 30, 0.92);
        border-radius: 22px;
        padding: 2rem;
        max-width: 1000px;
        margin: 0 auto;
        box-shadow: 0 0 30px rgba(0,0,0,0.35);
    }

    /* Title */
    h1 {
        text-align: center;
        font-size: 2.4rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        margin-bottom: 1.5rem;
        text-shadow: 0 0 15px rgba(0,173,181,0.5);
    }

    /* Labels */
    .stNumberInput label,
    .stSelectbox label {
        color: #cbd5e0 !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.2rem !important;
        transition: 0.2s ease;
    }

    .stNumberInput label:hover,
    .stSelectbox label:hover {
        color: #00adb5 !important;
    }

    /* Number Input */
    .stNumberInput input {
        background-color: #1a1a2e !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        padding: 0.5rem 0.8rem !important;
        transition: 0.2s ease;
    }

    .stNumberInput input:hover {
        border-color: #00adb5 !important;
    }

    /* Number Buttons */
    .stNumberInput button {
        background-color: #2d2d44 !important;
        border: 1px solid #334155 !important;
        color: white !important;
        border-radius: 6px !important;
    }

    .stNumberInput button:hover {
        background-color: #00adb5 !important;
    }

    /* Select Box */
    div[data-baseweb="select"] > div {
        background-color: #1a1a2e !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        min-height: 40px !important;
        transition: 0.2s ease;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: #00adb5 !important;
    }

    /* Dropdown */
    div[data-baseweb="popover"] > div {
        background-color: #1a1a2e !important;
        border-radius: 10px !important;
    }

    li[role="option"] {
        background-color: #1a1a2e !important;
        color: white !important;
    }

    li[role="option"]:hover {
        background-color: #00adb5 !important;
    }

    /* Predict Button */
    .stButton > button {
        width: 100%;
        height: 52px;
        border: none;
        border-radius: 50px;
        background: linear-gradient(135deg, #00adb5, #007cf0) !important;
        color: white !important;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-top: 1rem;
        transition: all 0.25s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        background: linear-gradient(135deg, #007a7f, #0059b3) !important;
    }

    /* Result Card */
    .result-card {
        background: #1a1a2e;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 18px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        text-align: center;
        box-shadow: 0 0 25px rgba(0,173,181,0.25);
        animation: fadeIn 0.4s ease;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(15px);
        }

        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .result-label {
        color: #9ca3af !important;
        font-size: 0.8rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .result-score {
        color: #00adb5 !important;
        font-size: 4rem;
        font-weight: 800;
        letter-spacing: 2px;
        margin-top: 8px;
    }

    .result-score span {
        color: #9ca3af !important;
        font-size: 1.2rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: gray;
        margin-top: 35px;
        font-size: 14px;
    }

    /* Responsive */
    @media (max-width: 768px) {

        .main .block-container {
            padding: 1rem;
        }

        h1 {
            font-size: 1.6rem !important;
        }

        .result-score {
            font-size: 3rem;
        }
    }

</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.markdown(
    "<h1>🎓 Student Score Predictor</h1>",
    unsafe_allow_html=True
)

# =====================================
# INPUT SECTION
# =====================================
col1, col2 = st.columns(2)

with col1:

    hours = st.number_input(
        "Hours Studied",
        min_value=0.0,
        max_value=24.0,
        value=5.0,
        step=0.5
    )

    attendance = st.number_input(
        "Attendance (%)",
        min_value=0.0,
        max_value=100.0,
        value=75.0,
        step=5.0
    )

    previous = st.number_input(
        "Previous Score",
        min_value=0.0,
        max_value=100.0,
        value=60.0,
        step=5.0
    )

    sleep = st.number_input(
        "Sleep Hours",
        min_value=0.0,
        max_value=12.0,
        value=7.0,
        step=0.5
    )

    motivation = st.selectbox(
        "Motivation Level",
        ["Low", "Medium", "High"]
    )

    teacher = st.selectbox(
        "Teacher Quality",
        ["Poor", "Average", "Good"]
    )

    school = st.selectbox(
        "School Type",
        ["Public", "Private"]
    )

with col2:

    internet = st.selectbox(
        "Internet Access",
        ["Yes", "No"]
    )

    income = st.selectbox(
        "Family Income",
        ["Low", "Medium", "High"]
    )

    parent = st.selectbox(
        "Parental Involvement",
        ["Low", "Medium", "High"]
    )

    education = st.selectbox(
        "Parent Education",
        ["School", "College"]
    )

    peer = st.selectbox(
        "Peer Influence",
        ["Negative", "Neutral", "Positive"]
    )

    resources = st.selectbox(
        "Learning Resources",
        ["Low", "Medium", "High"]
    )

    activities = st.selectbox(
        "Extracurricular Activities",
        ["Yes", "No"]
    )

# =====================================
# BUTTON
# =====================================
if st.button("🚀 PREDICT SCORE", use_container_width=True):

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

    input_df = input_df.reindex(
        columns=columns,
        fill_value=0
    )

    prediction = model.predict(input_df)

    final_score = max(
        40,
        min(100, prediction[0])
    )

    final_score = int(round(final_score))

    # RESULT CARD
    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-label">
                Predicted Exam Score
            </div>

            <div class="result-score">
                {final_score}<span>/100</span>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # Progress Bar
    st.progress(final_score / 100)

    # Performance Message
    if final_score >= 80:
        st.success("🌟 Excellent Performance Predicted!")
        st.balloons()

    elif final_score >= 60:
        st.success("👍 Good Performance Predicted!")

    else:
        st.success("📚 Student Needs Improvement!")

# =====================================
# FOOTER
# =====================================
st.markdown(
    """
    <div class="footer">
        Developed using Streamlit & Machine Learning
    </div>
    """,
    unsafe_allow_html=True
)
