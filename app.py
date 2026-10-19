import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page Config - makes it look pro
st.set_page_config(
    page_title="HealthTrack Pro",
    page_icon="💚",
    layout="wide"
)

# Custom CSS - this is the BEAUTY magic!
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 10px 30px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Beautiful Header
st.markdown("""
<div class="main-header">
    <h1>💚 HealthTrack Pro</h1>
    <p>Your Personal Wellness Journey, Beautifully Tracked ✨</p>
    <p><i>Built with 💜 by Anita Asuambuk</i></p>
</div>
""", unsafe_allow_html=True)

# Two columns - Create Account looks premium
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🌟 Create Your Account")
    st.markdown("Join thousands tracking their health!")
    
    with st.container():
        full_name = st.text_input("👤 Full Name", placeholder="Anita Asuambuk")
        email = st.text_input("📧 Email", placeholder="anita@example.com")
        age = st.number_input("🎂 Age", min_value=1, max_value=120, value=25)
        gender = st.selectbox("⚧ Gender", ["Female", "Male", "Other", "Prefer not to say"])
        
        if st.button("🚀 Start My Health Journey"):
            st.balloons()
            st.success(f"Welcome {full_name}! Your journey starts now! 🎉")

with col2:
    st.markdown("### 📊 Why HealthTrack?")
    
    # Metrics that look attractive
    m1, m2, m3 = st.columns(3)
    m1.metric("Users", "10K+", "↗️")
    m2.metric("Health Score", "98%", "💚")
    m3.metric("Rating", "4.9⭐", "🔥")
    
    st.markdown("---")
    st.markdown("""
    #### ✨ Features You'll Love:
    - 🥗 **Smart Nutrition Tracking**
    - 🏃‍♀️ **Fitness & Steps Monitor**
    - 😴 **Sleep & Mood Insights**
    - 📈 **Beautiful Charts**
    - 🎯 **Daily Goals & Streaks**
    """)
    
    # Sample chart to make it exciting
    st.markdown("#### 📈 Your Weekly Progress")
    chart_data = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Health Score': [70, 75, 80, 78, 85, 90, 95]
    })
    st.line_chart(chart_data.set_index('Day'))
    st.caption("Imagine YOUR data here! 🔥")

st.markdown("---")
st.markdown("<center><p>Made with 💜 by Anita | Inspiring Healthy Lives Everyday 🌍</p></center>", unsafe_allow_html=True)
