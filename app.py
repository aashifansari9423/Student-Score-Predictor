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
# PROFESSIONAL CUSTOM CSS
# =====================================
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Main block container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin-top: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    /* Title styling */
    h1 {
        text-align: center;
        font-size: 3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 2rem;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Input labels */
    .stNumberInput label, .stSelectbox label {
        font-weight: 600;
        color: #4a5568;
        font-size: 0.9rem;
        margin-bottom: 0.5rem;
    }
    
    /* Input fields */
    .stNumberInput input, div[data-baseweb="select"] > div {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        background-color: white;
    }
    
    .stNumberInput input:focus, div[data-baseweb="select"] > div:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        height: 55px;
        border: none;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.1rem;
        font-weight: 700;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 1rem;
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Result card styling */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem;
        border-radius: 20px;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        animation: slideUp 0.5s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: 1px;
    }
    
    .result-score {
        color: white;
        font-size: 4rem;
        font-weight: 800;
        margin: 1rem 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .score-unit {
        font-size: 1.5rem;
        font-weight: 500;
    }
    
    /* Performance message styling */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        animation: slideUp 0.5s ease-out;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #667eea, #764ba2, transparent);
    }
    
    /* Sidebar styling (if needed) */
    .css-1d391kg {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Metrics styling */
    .metric-container {
        background: #f7fafc;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .result-score {
            font-size: 2.5rem;
        }
        .result-title {
            font-size: 1.2rem;
        }
        h1 {
            font-size: 2rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.markdown("<h1>🎓 Student Score Predictor</h1>", unsafe_allow_html=True)

# =====================================
# TWO COLUMN LAYOUT FOR BETTER UI
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
        ["Low", "Medium", "High"],
        help="Student's motivation level"
    )
    
    teacher = st.selectbox(
        "👨‍🏫 Teacher Quality",
        ["Poor", "Average", "Good"],
        help="Quality of teaching"
    )
    
    school = st.selectbox(
        "🏫 School Type",
        ["Public", "Private"],
        help="Type of school"
    )

with col2:
    internet = st.selectbox(
        "🌐 Internet Access",
        ["Yes", "No"],
        help="Availability of internet at home"
    )
    
    income = st.selectbox(
        "💰 Family Income",
        ["Low", "Medium", "High"],
        help="Family income level"
    )
    
    parent = st.selectbox(
        "👪 Parental Involvement",
        ["Low", "Medium", "High"],
        help="Level of parental involvement in education"
    )
    
    education = st.selectbox(
        "🎓 Parent Education",
        ["School", "College"],
        help="Highest education level of parents"
    )
    
    peer = st.selectbox(
        "🤝 Peer Influence",
        ["Negative", "Neutral", "Positive"],
        help="Influence from peers"
    )
    
    resources = st.selectbox(
        "📚 Learning Resources",
        ["Low", "Medium", "High"],
        help="Availability of learning resources"
    )
    
    activities = st.selectbox(
        "⚽ Extracurricular Activities",
        ["Yes", "No"],
        help="Participation in extracurricular activities"
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
        # RESULT CARD - FIXED HTML
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
        # PERFORMANCE MESSAGE WITH METRICS
        # =====================================
        if final_score >= 85:
            st.balloons()
            st.success("🏆 **Outstanding Performance!** 🌟 You're a star student!")
            
            # Display encouraging metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Study Hours", f"{hours}/24", delta="Optimal" if hours >= 6 else "Increase")
            with col2:
                st.metric("Attendance", f"{attendance}%", delta="Good" if attendance >= 75 else "Needs improvement")
            with col3:
                st.metric("Sleep", f"{sleep} hours", delta="Healthy" if 7 <= sleep <= 9 else "Adjust")
                
        elif final_score >= 70:
            st.info("📈 **Good Performance!** Keep pushing for excellence!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Study Hours", f"{hours}/24", delta="On track")
            with col2:
                st.metric("Attendance", f"{attendance}%", delta="Keep it up")
                
        elif final_score >= 50:
            st.warning("📚 **Room for Improvement!** You can do better with more effort!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Study Hours", f"{hours}/24", delta="Needs increase" if hours < 5 else "Adequate")
            with col2:
                st.metric("Attendance", f"{attendance}%", delta="Needs improvement" if attendance < 70 else "Fair")
                
        else:
            st.error("⚠️ **Needs Significant Improvement!** Let's work together to improve!")
            
            st.markdown("""
            **Suggestions for improvement:**
            - 📚 Increase study hours (aim for 6-8 hours daily)
            - 📊 Improve attendance (target 80%+)
            - 😴 Get adequate sleep (7-9 hours)
            - 💪 Boost motivation through goal setting
            - 🤝 Seek positive peer groups
            """)
            
        # =====================================
        # ADDITIONAL INSIGHTS
        # =====================================
        st.markdown("---")
        st.markdown("### 📊 Key Insights")
        
        # Study hours impact
        if hours >= 8:
            st.success("✅ Excellent study hours! This positively impacts your score.")
        elif hours >= 5:
            st.info("ℹ️ Good study hours. Consider increasing to 8+ hours for better results.")
        else:
            st.warning("⚠️ Low study hours detected. Increasing study time could significantly improve scores.")
        
        # Attendance impact
        if attendance >= 85:
            st.success("✅ Great attendance! This strongly correlates with better performance.")
        elif attendance >= 70:
            st.info("ℹ️ Satisfactory attendance. Aim for 85%+ for optimal results.")
        else:
            st.warning("⚠️ Low attendance might be affecting your performance.")
            
        # Sleep impact
        if 7 <= sleep <= 9:
            st.success("✅ Optimal sleep schedule! This supports learning and memory.")
        elif sleep < 6:
            st.warning("⚠️ Insufficient sleep may affect concentration and performance.")
        elif sleep > 10:
            st.info("ℹ️ High sleep hours. Ensure it's not affecting study time.")
            
    except Exception as e:
        st.error(f"❌ Prediction error: {str(e)}")
        st.info("Please ensure all inputs are valid and try again.")
