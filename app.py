import streamlit as st
import joblib
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="centered"
)

# =========================
# LOAD MODEL
# =========================
model = joblib.load("student_model.pkl")
columns = joblib.load("model_columns.pkl")

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 2rem;
}

h1 {
    text-align: center;
    color: white;
    font-size: 50px !important;
    font-weight: bold;
}

.stButton > button {
    width: 100%;
    height: 55px;
    background: linear-gradient(to right,#7F5AF0,#2CB67D);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 20px;
    font-weight: bold;
}

.stButton > button:hover {
    opacity: 0.9;
}

.result-box {
    background: linear-gradient(to right,#7F5AF0,#2CB67D);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-top: 20px;
}

.big-text {
    font-size: 55px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.markdown("<h1>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)

st.markdown("###")

# =========================
# INPUTS
# =========================
hours = st.number_input("Hours Studied", 0.0, 24.0)

attendance = st.number_input("Attendance (%)", 0.0, 100.0)

previous = st.number_input("Previous Score", 0.0, 100.0)

sleep = st.number_input("Sleep Hours", 0.0, 12.0)

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

# =========================
# BUTTON
# =========================
if st.button("🚀 Predict Score"):

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

    # RESULT BOX
    st.markdown(f'''
    <div class="result-box">

        <h2>Predicted Exam Score</h2>

        <div class="big-text">
            {final_score}/100
        </div>

    </div>
    ''', unsafe_allow_html=True)

    # PERFORMANCE MESSAGE
    if final_score >= 80:
        st.success("🌟 Excellent Performance!")
        st.balloons()

    elif final_score >= 60:
        st.info("👍 Good Performance!")

    else:
        st.warning("📚 Needs Improvement!")
