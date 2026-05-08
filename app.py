import streamlit as st
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

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
@st.cache_resource
def load_models():
    model = joblib.load("student_model.pkl")
    columns = joblib.load("model_columns.pkl")
    return model, columns

model, columns = load_models()

# =====================================
# SESSION STATE
# =====================================
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []

# =====================================
# CUSTOM CSS - PROFESSIONAL DARK THEME
# =====================================
st.markdown("""
<style>
    /* Force all text white */
    .stApp, .stApp * {
        color: #ffffff !important;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    /* Main container */
    .main .block-container {
        background: rgba(18, 18, 30, 0.92);
        border-radius: 16px;
        padding: 2rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    /* Remove focus rings */
    *:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Title */
    h1 {
        text-align: center;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-bottom: 2rem;
    }
    
    h2, h3 {
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }
    
    /* Labels */
    .stNumberInput label, .stSelectbox label {
        color: #cbd5e0 !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        margin-bottom: 0.2rem !important;
    }
    
    /* Input fields */
    .stNumberInput input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        padding: 0.4rem 0.8rem !important;
    }
    
    .stNumberInput input:hover {
        border-color: #00adb5 !important;
    }
    
    /* Number buttons */
    .stNumberInput button {
        background-color: #2d2d44 !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
    }
    
    .stNumberInput button:hover {
        background-color: #00adb5 !important;
    }
    
    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #1a1a2e !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        min-height: 36px !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #00adb5 !important;
    }
    
    /* Dropdown */
    div[data-baseweb="popover"] > div {
        background-color: #1a1a2e !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    
    li[role="option"]:hover {
        background-color: #00adb5 !important;
    }
    
    /* Button */
    .stButton > button {
        width: 100%;
        background: #00adb5 !important;
        color: white !important;
        border: none;
        border-radius: 50px !important;
        padding: 0.6rem !important;
        font-weight: 600 !important;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #007a7f !important;
        transform: translateY(-2px);
    }
    
    /* Result Card */
    .result-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 2px solid #00adb5;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        margin: 1.5rem 0;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .result-label {
        color: #aaaaaa !important;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .result-score {
        color: #00adb5 !important;
        font-size: 3rem;
        font-weight: 800;
    }
    
    /* Success/Info/Warning */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 10px;
        padding: 0.8rem;
        margin: 0.5rem 0;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: #334155;
    }
    
    /* Columns */
    div[data-testid="column"] {
        padding: 0 0.5rem;
    }
    
    /* Mobile */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        h1 {
            font-size: 1.5rem !important;
        }
        div[data-testid="column"] {
            padding: 0 0.3rem;
        }
        .result-score {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.markdown("<h1>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)

# =====================================
# TWO COLUMN INPUTS
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
    
    # Prepare data
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
    
    # Prediction
    input_df = pd.DataFrame([data])
    input_df = pd.get_dummies(input_df)
    input_df = input_df.reindex(columns=columns, fill_value=0)
    
    prediction = model.predict(input_df)
    final_score = max(40, min(100, prediction[0]))
    final_score = int(round(final_score))
    
    # Save to history
    st.session_state.prediction_history.append({
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'score': final_score,
        'hours': hours,
        'attendance': attendance
    })
    
    # Keep only last 5 records
    if len(st.session_state.prediction_history) > 5:
        st.session_state.prediction_history = st.session_state.prediction_history[-5:]
    
    # =====================================
    # RESULT CARD
    # =====================================
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">PREDICTED EXAM SCORE</div>
        <div class="result-score">{final_score}<span style="font-size: 1rem;"> / 100</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # =====================================
    # PERFORMANCE ASSESSMENT
    # =====================================
    if final_score >= 85:
        st.success("🏆 EXCEPTIONAL PERFORMANCE - Outstanding results!")
        st.balloons()
    elif final_score >= 70:
        st.success("📈 GOOD PERFORMANCE - Keep improving!")
    elif final_score >= 55:
        st.info("📚 SATISFACTORY PERFORMANCE - Room for improvement")
    else:
        st.warning("⚠️ NEEDS IMPROVEMENT - Review recommendations below")
    
    # =====================================
    # SMART RECOMMENDATIONS
    # =====================================
    st.markdown("### Recommendations")
    
    rec_count = 0
    if hours < 6:
        st.info("📖 Increase study hours to 6-8 hours daily")
        rec_count += 1
    if attendance < 75:
        st.info("📊 Improve attendance to 80% or higher")
        rec_count += 1
    if sleep < 7:
        st.info("😴 Get 7-9 hours of sleep for better focus")
        rec_count += 1
    if motivation == "Low":
        st.info("💪 Set daily goals to boost motivation")
        rec_count += 1
    if teacher == "Poor":
        st.info("👨‍🏫 Seek additional tutoring or online resources")
        rec_count += 1
    if resources == "Low":
        st.info("📚 Utilize free online learning materials")
        rec_count += 1
    if peer == "Negative":
        st.info("🤝 Join positive study groups for better environment")
        rec_count += 1
    
    if rec_count == 0:
        st.success("✅ Excellent habits! Maintain your current routine")

# =====================================
# RECENT PREDICTIONS (Simple)
# =====================================
if st.session_state.prediction_history:
    st.markdown("---")
    st.markdown("### Recent Predictions")
    
    # Simple table
    history_df = pd.DataFrame(st.session_state.prediction_history)
    history_df = history_df[['timestamp', 'score', 'hours', 'attendance']]
    history_df.columns = ['Time', 'Score', 'Study Hrs', 'Attend %']
    
    st.dataframe(history_df, use_container_width=True, hide_index=True)

# =====================================
# FOOTER
# =====================================
st.markdown("---")
st.caption("© 2024 Student Score Predictor | AI-Powered Academic Tool")
