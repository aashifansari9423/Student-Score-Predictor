import streamlit as st
import joblib
import pandas as pd

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
# CUSTOM CSS
# =====================================
st.markdown("""
<style>

body {
    background-color: #0E1117;
}

.main {
    background: linear-gradient(to bottom right, #111827, #0F172A);
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1 {
    text-align: center;
    font-size: 52px !important;
    color: white;
    font-weight: bold;
    margin-bottom: 30px;
}

/* Input Box */
.stNumberInput input {
    border-radius: 10px !important;
}

/* Select Box */
div[data-baseweb="select"] > div {
    border-radius: 10px !important;
}

/* Button */
.stButton > button {
    width: 100%;
    height: 55px;
    border: none;
    border-radius: 14px;
    background: linear-gradient(to right, #2563EB, #7C3AED);
    color: white;
    font-size: 20px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    opacity: 0.95;
}

/* Result Card */
.result-card {
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    padding: 35px;
    border-radius: 22px;
    text-align: center;
    margin-top: 30px;
    box-shadow: 0px 0px 25px rgba(0,0,0,0.35);
}

.result-title {
    color: white;
    font-size: 30px;
    font-weight: bold;
}

.result-score {
    color: white;
    font-size: 75px;
    font-weight: bold;
    margin-top: 10px;
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
# INPUT FIELDS
# =====================================
hours = st.number_input(
    "Hours Studied",
    0.0,
    24.0
)

attendance = st.number_input(
    "Attendance (%)",
    0.0,
    100.0
)

previous = st.number_input(
    "Previous Score",
    0.0,
    100.0
)

sleep = st.number_input(
    "Sleep Hours",
    0.0,
    12.0
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
# PREDICT BUTTON
# =====================================
if st.button("🚀 Predict Score"):

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

    # DataFrame
    input_df = pd.DataFrame([data])

    # Encoding
    input_df = pd.get_dummies(input_df)

    # Match Columns
    input_df = input_df.reindex(
        columns=columns,
        fill_value=0
    )

    # Prediction
    prediction = model.predict(input_df)

    # Score Fix
    final_score = max(
        40,
        min(100, prediction[0])
    )

    final_score = int(round(final_score))

    # =====================================
    # RESULT CARD
    # =====================================
    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-title">
                Predicted Exam Score
            </div>

            <div class="result-score">
                {final_score}/100
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================
    # PERFORMANCE MESSAGE
    # =====================================
    if final_score >= 80:
        st.success("🌟 Excellent Performance!")
        st.balloons()

    elif final_score >= 60:
        st.info("👍 Good Performance!")

    else:
        st.warning("📚 Needs Improvement!")
