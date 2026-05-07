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
try:
    model = joblib.load("student_model.pkl")
    columns = joblib.load("model_columns.pkl")
except:
    st.error("⚠️ Model files not found! Please ensure 'student_model.pkl' and 'model_columns.pkl' exist.")
    st.stop()

# =====================================
# DARK THEME CSS - SAB KUCH DIKHEGA
# =====================================
st.markdown("""
<style>
    /* Main dark background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    }
    
    /* Main container */
    .main .block-container {
        background: rgba(18, 18, 30, 0.95);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Title */
    h1 {
        text-align: center;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
    }
    
    /* Labels - WHITE COLOR */
    .stNumberInput label, .stSelectbox label {
        color: #e2e8f0 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Input fields - VISIBLE */
    .stNumberInput input {
        background-color: #1e1e2e !important;
        color: white !important;
        border: 1px solid #4a5568 !important;
        border-radius: 10px !important;
        padding: 0.5rem !important;
    }
    
    .stNumberInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Select boxes - VISIBLE */
    div[data-baseweb="select"] > div {
        background-color: #1e1e2e !important;
        border: 1px solid #4a5568 !important;
        border-radius: 10px !important;
        color: white !important;
    }
    
    div[data-baseweb="select"] input {
        color: white !important;
    }
    
    /* Dropdown menu */
    div[data-baseweb="popover"] div {
        background-color: #1e1e2e !important;
        border: 1px solid #4a5568 !important;
    }
    
    li[role="option"] {
        color: white !important;
    }
    
    li[role="option"]:hover {
        background-color: #2d2d44 !important;
    }
    
    /* Button */
    .stButton > button {
        width: 100%;
        height: 55px;
        border: none;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        margin-top: 1rem;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Result Card */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
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
    
    .result-title {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .result-score {
        color: white;
        font-size: 3.5rem;
        font-weight: bold;
    }
    
    .score-unit {
        font-size: 1.2rem;
    }
    
    /* Success/Info/Warning messages */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    /* Divider */
    hr {
        margin: 1.5rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #667eea, #764ba2, transparent);
    }
    
    /* Metric cards */
    .metric-card {
        background: #1e1e2e;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #2d2d44;
    }
    
    /* Number input increment buttons */
    .stNumberInput button {
        background-color: #2d2d44 !important;
        border-color: #4a5568 !important;
        color: white !important;
    }
    
    /* Placeholder text */
    ::placeholder {
        color: #a0aec0 !important;
    }
    
    /* Column spacing */
    div[data-testid="column"] {
        padding: 0 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.markdown("<h1>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)

# =====================================
# TWO COLUMN LAYOUT
# =====================================
col1, col2 = st.columns(2)

with col1:
    hours = st.number_input(
        "📚 Hours Studied",
        min_value=0.0,
        max_value=24.0,
        value=5.0,
        step=0.5,
        help="Number of hours student studies per day"
    )
    
    attendance = st.number_input(
        "📊 Attendance (%)",
        min_value=0.0,
        max_value=100.0,
        value=75.0,
        step=5.0,
        help="Student's attendance percentage"
    )
    
    previous = st.number_input(
        "📈 Previous Score",
        min_value=0.0,
        max_value=100.0,
        value=60.0,
        step=5.0,
        help="Previous exam score"
    )
    
    sleep = st.number_input(
        "😴 Sleep Hours",
        min_value=0.0,
        max_value=12.0,
        value=7.0,
        step=0.5,
        help="Average sleep hours per day"
    )
    
    motivation = st.selectbox(
        "💪 Motivation Level",
        ["Low", "Medium", "High"]
    )
    
    teacher = st.selectbox(
        "👨‍🏫 Teacher Quality",
        ["Poor", "Average", "Good"]
    )
    
    school = st.selectbox(
        "🏫 School Type",
        ["Public", "Private"]
    )

with col2:
    internet = st.selectbox(
        "🌐 Internet Access",
        ["Yes", "No"]
    )
    
    income = st.selectbox(
        "💰 Family Income",
        ["Low", "Medium", "High"]
    )
    
    parent = st.selectbox(
        "👪 Parental Involvement",
        ["Low", "Medium", "High"]
    )
    
    education = st.selectbox(
        "🎓 Parent Education",
        ["School", "College"]
    )
    
    peer = st.selectbox(
        "🤝 Peer Influence",
        ["Negative", "Neutral", "Positive"]
    )
    
    resources = st.selectbox(
        "📚 Learning Resources",
        ["Low", "Medium", "High"]
    )
    
    activities = st.selectbox(
        "⚽ Extracurricular Activities",
        ["Yes", "No"]
    )

# =====================================
# PREDICT BUTTON
# =====================================
if st.button("🚀 PREDICT SCORE", use_container_width=True):
    
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
    
    # Create DataFrame
    input_df = pd.DataFrame([data])
    
    # One-hot encoding
    input_df = pd.get_dummies(input_df)
    
    # Align with training columns
    input_df = input_df.reindex(columns=columns, fill_value=0)
    
    # Make prediction
    try:
        prediction = model.predict(input_df)
        
        # Clamp prediction between 0-100
        final_score = int(round(np.clip(prediction[0], 0, 100)))
        
        # =====================================
        # RESULT CARD
        # =====================================
        st.markdown(f"""
        <div class="result-card">
            <div class="result-title">
                🎯 Predicted Exam Score
            </div>
            <div class="result-score">
                {final_score}<span class="score-unit">/100</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # =====================================
        # PERFORMANCE MESSAGE
        # =====================================
        if final_score >= 85:
            st.balloons()
            st.success("🏆 **Outstanding Performance!** 🌟 Excellent work!")
            
            # Feedback
            st.info(f"💡 **Tip:** Your current study habits are working well! Maintain {hours} hours of study and {attendance}% attendance.")
            
        elif final_score >= 70:
            st.info("📈 **Good Performance!** Keep pushing for excellence!")
            
            st.info(f"💡 **Tip:** Try increasing study hours to 8+ for even better results. Current: {hours} hours")
            
        elif final_score >= 50:
            st.warning("📚 **Room for Improvement!** You can do better!")
            
            st.warning(f"💡 **Tip:** Consider increasing study hours (current: {hours}) and attendance (current: {attendance}%)")
            
        else:
            st.error("⚠️ **Needs Significant Improvement!** Let's work together!")
            
            st.markdown("""
            **📝 Suggestions:**
            - 📚 Increase study hours to 6-8 hours daily
            - 📊 Improve attendance to 80%+
            - 😴 Maintain 7-9 hours of sleep
            - 💪 Set daily study goals
            """)
            
    except Exception as e:
        st.error(f"❌ Prediction error: {str(e)}")
        st.info("Please check all inputs and try again.")
