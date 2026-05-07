import streamlit as st
import joblib
import pandas as pd

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="wide"
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
    background: linear-gradient(to right, #0f172a, #111827);
    color: white;
}

h1 {
    text-align: center;
    font-size: 50px !important;
    font-weight: bold;
    color: #ffffff;
}

.stMarkdown {
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.3);
    backdrop-filter: blur(10px);
}

.result-card {
    background: linear-gradient(135deg,#6C63FF,#3B82F6);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    color: white;
    margin-top: 20px;
    box-shadow: 0px 0px 25px rgba(108,99,255,0.5);
}

.big-score {
    font-size: 70px;
    font-weight: bold;
}

.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 12px;
    border: none;
    background: linear-gradient(to right,#6C63FF,#3B82F6);
    color: white;
    font-size: 20px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.03);
    background: linear-gradient(to right,#574bdb,#2563eb);
}

div[data-baseweb="select"] > div {
    border-radius: 10px;
}

input {
    border-radius: 10px !important;
}

.footer {
    text-align: center;
    margin-top: 50px;
    color: gray;
    font-size: 15px;
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

st.markdown("---")

# =====================================
# LAYOUT
# =====================================
left_col, right_col = st.columns([2,1])

# =====================================
# INPUT SECTION
# =====================================
with left_col:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📋 Enter Student Details")

    col1, col2 = st.columns(2)

    with col1:
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

    predict_button = st.button("🚀 Predict Score")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# PREDICTION SECTION
# =====================================
with right_col:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("📊 Prediction Result")

    if predict_button:

        # Create Data
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
        input_df = input_df.reindex(
            columns=columns,
            fill_value=0
        )

        # Prediction
        prediction = model.predict(input_df)

        # Score Range Fix
        final_score = max(
            40,
            min(100, prediction[0])
        )

        final_score = int(round(final_score))

        # Result Card
        st.markdown(f"""
        <div class="result-card">

            <h2>Predicted Score</h2>

            <div class="big-score">
                {final_score}
            </div>

            <h3>/ 100</h3>

        </div>
        """, unsafe_allow_html=True)

        # Progress Bar
        st.progress(final_score)

        # Performance Messages
        if final_score >= 80:
            st.success("🌟 Excellent Performance Predicted!")
            st.balloons()

        elif final_score >= 60:
            st.info("👍 Good Performance Predicted!")

        else:
            st.warning("📚 Student Needs Improvement!")

    else:
        st.info("Enter details and click Predict Score.")

    st.markdown('</div>', unsafe_allow_html=True)

# =====================================
# FOOTER
# =====================================
st.markdown("""
<div class="footer">
    Developed using Streamlit & Machine Learning
</div>
""", unsafe_allow_html=True)
