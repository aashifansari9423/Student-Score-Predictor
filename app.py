import streamlit as st
import joblib
import pandas as pd
import numpy as np
import json
from datetime import datetime

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
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
# SESSION STATE FOR HISTORY
# =====================================
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = []
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""

# =====================================
# CUSTOM CSS
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
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(18, 18, 30, 0.95);
        border-right: 1px solid #334155;
    }
    
    /* Main container */
    .main .block-container {
        background: rgba(18, 18, 30, 0.92);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.5rem;
    }
    
    /* Remove focus rings */
    *:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Title */
    h1, h2, h3 {
        color: #ffffff !important;
    }
    
    /* Labels */
    .stNumberInput label, .stSelectbox label {
        color: #cbd5e0 !important;
        font-weight: 500 !important;
        font-size: 0.8rem !important;
        transition: color 0.2s ease;
    }
    
    .stNumberInput label:hover, .stSelectbox label:hover {
        color: #00adb5 !important;
    }
    
    /* Input fields */
    .stNumberInput input {
        background-color: #1a1a2e !important;
        color: #ffffff !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 0.4rem 0.8rem !important;
        transition: border 0.2s ease;
    }
    
    .stNumberInput input:hover {
        border-color: #00adb5 !important;
    }
    
    /* Number buttons */
    .stNumberInput button {
        background-color: #2d2d44 !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
        transition: background 0.2s ease;
    }
    
    .stNumberInput button:hover {
        background-color: #00adb5 !important;
    }
    
    /* Select boxes */
    div[data-baseweb="select"] > div {
        background-color: #1a1a2e !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        min-height: 36px !important;
        transition: border 0.2s ease;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #00adb5 !important;
    }
    
    /* Dropdown */
    div[data-baseweb="popover"] > div {
        background-color: #1a1a2e !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    
    li[role="option"]:hover {
        background-color: #00adb5 !important;
    }
    
    /* Button */
    .stButton > button {
        background: #00adb5 !important;
        color: white;
        border: none;
        border-radius: 50px !important;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #007a7f !important;
        transform: translateY(-2px);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00adb5 !important;
        font-size: 1.8rem !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        h1 {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# SIDEBAR - STUDENT PROFILE
# =====================================
with st.sidebar:
    st.markdown("## 👤 Student Profile")
    st.session_state.student_name = st.text_input("Student Name", value=st.session_state.student_name, placeholder="Enter your name")
    
    st.markdown("---")
    st.markdown("### 🎯 Target Score")
    target_score = st.slider("Set your target", 0, 100, 75)
    
    st.markdown("---")
    st.markdown("### 📊 Quick Stats")
    
    if st.session_state.prediction_history:
        avg_score = np.mean([p['score'] for p in st.session_state.prediction_history])
        best_score = max([p['score'] for p in st.session_state.prediction_history])
        total_predictions = len(st.session_state.prediction_history)
        
        st.metric("Average Score", f"{avg_score:.1f}")
        st.metric("Best Score", f"{best_score}")
        st.metric("Total Predictions", total_predictions)
    else:
        st.info("No predictions yet")
    
    st.markdown("---")
    st.markdown("### 💡 Pro Tips")
    st.caption("📚 Study 6-8 hours daily")
    st.caption("📊 Maintain 80%+ attendance")
    st.caption("😴 Sleep 7-9 hours")
    st.caption("💪 Stay motivated")
    
    st.markdown("---")
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.prediction_history = []
        st.rerun()

# =====================================
# MAIN TITLE
# =====================================
st.markdown("<h1 style='text-align: center;'>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)

# =====================================
# MAIN CONTENT - TWO COLUMNS
# =====================================
col1, col2 = st.columns(2, gap="medium")

with col1:
    st.markdown("### 📚 Academic Details")
    hours = st.number_input("Hours Studied", min_value=0.0, max_value=24.0, value=5.0, step=0.5)
    attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=75.0, step=5.0)
    previous = st.number_input("Previous Score", min_value=0.0, max_value=100.0, value=60.0, step=5.0)
    sleep = st.number_input("Sleep Hours", min_value=0.0, max_value=12.0, value=7.0, step=0.5)
    
    st.markdown("### 🎭 Personal Factors")
    motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
    teacher = st.selectbox("Teacher Quality", ["Poor", "Average", "Good"])
    school = st.selectbox("School Type", ["Public", "Private"])

with col2:
    st.markdown("### 🏠 Environmental Factors")
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
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_clicked = st.button("🚀 PREDICT SCORE", use_container_width=True)

if predict_clicked:
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
    
    input_df = pd.DataFrame([data])
    input_df = pd.get_dummies(input_df)
    input_df = input_df.reindex(columns=columns, fill_value=0)
    
    prediction = model.predict(input_df)
    final_score = max(40, min(100, prediction[0]))
    final_score = int(round(final_score))
    
    # Save to history
    st.session_state.prediction_history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'score': final_score,
        'hours': hours,
        'attendance': attendance,
        'previous': previous,
        'sleep': sleep
    })
    
    # =====================================
    # RESULT CARD
    # =====================================
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #1a1a2e, #16213e); border: 2px solid #00adb5; border-radius: 20px; padding: 1.5rem; text-align: center;'>
            <div style='color: #aaaaaa; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 2px;'>PREDICTED EXAM SCORE</div>
            <div style='color: #00adb5; font-size: 3.5rem; font-weight: 800;'>{final_score}<span style='font-size: 1.2rem;'>/100</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    # =====================================
    # PERFORMANCE MESSAGE
    # =====================================
    if final_score >= 85:
        st.success(f"🎉 Outstanding! {st.session_state.student_name if st.session_state.student_name else 'Student'} scored {final_score}/100")
        st.balloons()
    elif final_score >= 70:
        st.success(f"📈 Good job! Score: {final_score}/100")
    elif final_score >= 50:
        st.info(f"📚 Keep working! Score: {final_score}/100")
    else:
        st.warning(f"⚠️ Need improvement! Score: {final_score}/100")
    
    # =====================================
    # SMART TIPS
    # =====================================
    st.markdown("### 💡 Smart Recommendations")
    
    tips = []
    if hours < 6:
        tips.append("📚 **Increase study hours** - Aim for 6-8 hours daily (+15% score potential)")
    if attendance < 75:
        tips.append("📊 **Improve attendance** - Regular classes boost scores by 10-15%")
    if sleep < 7:
        tips.append("😴 **Get more sleep** - 7-9 hours improves memory and focus")
    if motivation == "Low":
        tips.append("💪 **Boost motivation** - Set small goals and reward yourself")
    if teacher == "Poor":
        tips.append("👨‍🏫 **Seek extra help** - Consider tutoring or online resources")
    if resources == "Low":
        tips.append("📖 **Get better resources** - Use online materials and library")
    if peer == "Negative":
        tips.append("🤝 **Change study group** - Surround yourself with motivated peers")
    
    if tips:
        for tip in tips:
            st.info(tip)
    else:
        st.success("🌟 Excellent habits! You're on the right track!")
    
    # =====================================
    # PROGRESS TOWARDS TARGET
    # =====================================
    st.markdown("### 🎯 Target Progress")
    progress = min(final_score / target_score, 1.0)
    st.progress(progress)
    st.caption(f"Target: {target_score} | Current: {final_score} | {progress*100:.0f}% achieved")
    
    # =====================================
    # FEATURE IMPACT
    # =====================================
    st.markdown("### 📊 Key Factors Impact")
    
    factors = {
        "Study Hours": "High" if hours >= 7 else "Medium" if hours >= 5 else "Low",
        "Attendance": "High" if attendance >= 85 else "Medium" if attendance >= 70 else "Low",
        "Sleep": "Optimal" if 7 <= sleep <= 9 else "Suboptimal",
        "Motivation": motivation,
        "Resources": resources
    }
    
    for factor, status in factors.items():
        if status in ["High", "Optimal", "Good"]:
            st.success(f"✓ {factor}: {status}")
        elif status in ["Medium", "Average"]:
            st.info(f"• {factor}: {status}")
        else:
            st.warning(f"⚠ {factor}: {status} - Needs improvement")

# =====================================
# PREDICTION HISTORY
# =====================================
if st.session_state.prediction_history:
    st.markdown("---")
    st.markdown("### 📈 Prediction History")
    
    history_df = pd.DataFrame(st.session_state.prediction_history)
    
    # Simple bar chart without plotly
    st.dataframe(history_df[['timestamp', 'score', 'hours', 'attendance', 'sleep']], use_container_width=True)
    
    # Show score trend as text
    st.markdown("**Score Trend:**")
    scores = [p['score'] for p in st.session_state.prediction_history]
    if len(scores) > 1:
        if scores[-1] > scores[-2]:
            st.success("📈 Score increased! Keep it up!")
        elif scores[-1] < scores[-2]:
            st.warning("📉 Score decreased. Review the recommendations above.")
        else:
            st.info("➡️ Score stable. Try to improve further.")

# =====================================
# DOWNLOAD REPORT
# =====================================
if predict_clicked and final_score:
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        report_data = {
            "student_name": st.session_state.student_name,
            "predicted_score": final_score,
            "target_score": target_score,
            "inputs": data,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "recommendations": tips if 'tips' in locals() else []
        }
        
        json_str = json.dumps(report_data, indent=2)
        st.download_button(
            label="📥 Download Report (JSON)",
            data=json_str,
            file_name=f"score_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    with col2:
        st.info("📊 Share your results with teachers!")
    
    with col3:
        if final_score >= 70:
            st.success("🏆 Keep the momentum!")

# =====================================
# FOOTER
# =====================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666; font-size: 0.8rem;'>Powered by AI | Student Score Predictor</p>",
    unsafe_allow_html=True
)
