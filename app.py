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
@st.cache_resource
def load_models():
    model = joblib.load("student_model.pkl")
    columns = joblib.load("model_columns.pkl")
    return model, columns

model, columns = load_models()

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
        border-radius: 20px;
        padding: 2rem;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    /* Remove all focus rings */
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
        letter-spacing: -0.5px;
    }
    
    /* Labels */
    .stNumberInput label, .stSelectbox label {
        color: #cbd5e0 !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        margin-bottom: 0.3rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Input fields */
    .stNumberInput input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 0.5rem 0.8rem !important;
        font-size: 0.9rem !important;
        transition: all 0.2s ease;
    }
    
    .stNumberInput input:hover {
        border-color: #00adb5 !important;
    }
    
    /* Number buttons */
    .stNumberInput button {
        background-color: #2d2d44 !important;
        border: 1px solid #334155 !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        transition: all 0.2s ease;
    }
    
    .stNumberInput button:hover {
        background-color: #00adb5 !important;
    }
    
    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #1a1a2e !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        min-height: 38px !important;
        padding: 0 10px !important;
        transition: all 0.2s ease;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #00adb5 !important;
    }
    
    div[data-baseweb="select"] input {
        color: #ffffff !important;
        font-size: 0.9rem !important;
    }
    
    /* Dropdown menu */
    div[data-baseweb="popover"] > div {
        background-color: #1a1a2e !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    
    li[role="option"] {
        color: #ffffff !important;
        background-color: #1a1a2e !important;
        padding: 10px 15px !important;
        font-size: 0.85rem !important;
        transition: all 0.2s ease;
    }
    
    li[role="option"]:hover {
        background-color: #00adb5 !important;
    }
    
    li[role="option"][aria-selected="true"] {
        background-color: #00adb5 !important;
    }
    
    /* Predict Button */
    .stButton > button {
        width: 100%;
        height: 52px;
        background: #00adb5 !important;
        color: white !important;
        border: none;
        border-radius: 50px !important;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin-top: 1.5rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        background: #007a7f !important;
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0, 173, 181, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Result Card */
    .result-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 2px solid #00adb5;
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        margin: 1.5rem 0;
        animation: slideDown 0.4s ease-out;
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-label {
        color: #888888 !important;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 0.5rem;
    }
    
    .result-score {
        color: #00adb5 !important;
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    .result-score span {
        font-size: 1.2rem;
        color: #666666 !important;
    }
    
    /* Message boxes */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 12px;
        padding: 1rem;
        margin: 0.8rem 0;
        font-weight: 500;
    }
    
    .stSuccess {
        background-color: rgba(0, 173, 181, 0.1);
        border-left: 4px solid #00adb5;
    }
    
    .stInfo {
        background-color: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
    }
    
    .stWarning {
        background-color: rgba(245, 158, 11, 0.1);
        border-left: 4px solid #f59e0b;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #334155, transparent);
    }
    
    /* Columns spacing */
    div[data-testid="column"] {
        padding: 0 0.6rem;
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1.2rem;
        }
        
        h1 {
            font-size: 1.5rem !important;
        }
        
        .result-score {
            font-size: 2.5rem;
        }
        
        div[data-testid="column"] {
            padding: 0 0.3rem;
        }
        
        .stNumberInput input, div[data-baseweb="select"] > div {
            min-height: 42px;
        }
        
        .stButton > button {
            height: 48px;
            font-size: 0.9rem;
        }
    }
    
    /* Small devices */
    @media (max-width: 480px) {
        .result-score {
            font-size: 2rem;
        }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #00adb5;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #007a7f;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.markdown("<h1>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)

# =====================================
# INPUT FIELDS - TWO COLUMNS
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
    
    # Prepare input data
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
    
    # Make prediction
    input_df = pd.DataFrame([data])
    input_df = pd.get_dummies(input_df)
    input_df = input_df.reindex(columns=columns, fill_value=0)
    
    prediction = model.predict(input_df)
    final_score = max(40, min(100, prediction[0]))
    final_score = int(round(final_score))
    
    # =====================================
    # RESULT DISPLAY
    # =====================================
    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">PREDICTED EXAM SCORE</div>
        <div class="result-score">{final_score}<span> / 100</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # =====================================
    # PERFORMANCE ASSESSMENT
    # =====================================
    if final_score >= 85:
        st.success("🏆 EXCEPTIONAL PERFORMANCE")
        st.balloons()
    elif final_score >= 70:
        st.success("📈 GOOD PERFORMANCE")
    elif final_score >= 55:
        st.info("📚 SATISFACTORY PERFORMANCE")
    else:
        st.warning("⚠️ NEEDS IMPROVEMENT")
    
    # =====================================
    # RECOMMENDATIONS
    # =====================================
    recommendations = []
    
    if hours < 6:
        recommendations.append("Increase study hours to 6-8 hours daily")
    if attendance < 75:
        recommendations.append("Improve attendance to 80% or higher")
    if sleep < 7:
        recommendations.append("Get 7-9 hours of sleep for better focus")
    if motivation == "Low":
        recommendations.append("Set daily goals to boost motivation")
    if teacher == "Poor":
        recommendations.append("Seek additional tutoring or online resources")
    if resources == "Low":
        recommendations.append("Utilize free online learning materials")
    if peer == "Negative":
        recommendations.append("Join positive study groups")
    if previous < 50:
        recommendations.append("Focus on strengthening fundamental concepts")
    
    if recommendations:
        st.markdown("### Recommendations")
        for rec in recommendations:
            st.info(f"• {rec}")
    else:
        st.success("✅ Excellent study habits! Maintain your routine")

# =====================================
# FOOTER
# =====================================
st.markdown("---")
st.caption("Student Score Predictor | Powered by Machine Learning")
