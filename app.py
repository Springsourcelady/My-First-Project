import streamlit as st
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="HealthTrack Pro", page_icon="💚", layout="wide")

# --- BEAUTIFUL STYLES ---
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 0;
    }
    .main-header p {
        opacity: 0.9;
        margin-top: 0.5rem;
        font-size: 1.1rem;
    }
    .metric-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .med-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'medications' not in st.session_state:
    st.session_state.medications = []
if 'taken_today' not in st.session_state:
    st.session_state.taken_today = {}

# --- HEADER ---
st.markdown("""
<div class="main-header">
    <h1>💚 HealthTrack Pro</h1>
    <p>Your Personal Wellness Journey, Beautifully Tracked ✨</p>
    <p style="font-size:0.9rem; margin-top:1rem;">Built with 💜 by Anita Asuambuk</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.2, 1])

with left:
    st.markdown("### 🌟 Create Your Account")
    st.write("Join thousands tracking their health!")
    with st.form("account_form"):
        name = st.text_input("👤 Full Name", placeholder="Anita Asuambuk")
        email = st.text_input("📧 Email", placeholder="mpassion54@gmail.com")
        submitted = st.form_submit_button("Create Account →", use_container_width=True)
        if submitted:
            st.success(f"Welcome {name}! Account created! 🎉")

    st.divider()
    st.markdown("### 💊 Medication Reminder Center")
    st.write("Never miss a dose again!")

    with st.form("med_form"):
        col1, col2 = st.columns(2)
        with col1:
            med_name = st.text_input("Medication Name", placeholder="e.g. Vitamin C")
            dosage = st.text_input("Dosage", placeholder="e.g. 500mg, 1 tablet")
        with col2:
            med_time = st.time_input("Daily Time", value=datetime.now().time())
            frequency = st.selectbox("Frequency", ["Daily", "Twice a day", "Weekly", "As needed"])
        
        add_med = st.form_submit_button("➕ Add Medication", use_container_width=True)
        if add_med and med_name:
            st.session_state.medications.append({
                "name": med_name,
                "dosage": dosage,
                "time": med_time.strftime("%H:%M"),
                "frequency": frequency,
                "added": datetime.now().strftime("%Y-%m-%d")
            })
            st.success(f"Added {med_name}!")
            time.sleep(0.5)
            st.rerun()

    # Display Medications
    if st.session_state.medications:
        st.markdown(f"#### Your Medications ({len(st.session_state.medications)})")
        for i, med in enumerate(st.session_state.medications):
            is_taken = st.session_state.taken_today.get(i, False)
            st.markdown(f"""
            <div class="med-card">
                <b>💊 {med['name']}</b> - {med['dosage']}<br>
                ⏰ {med['time']} | 🔁 {med['frequency']}
            </div>
            """, unsafe_allow_html=True)
            col_a, col_b = st.columns([1,1])
            with col_a:
                if st.button("✅ Taken Today" if not is_taken else "✓ Taken!", key=f"taken_{i}", use_container_width=True, disabled=is_taken):
                    st.session_state.taken_today[i] = True
                    st.rerun()
            with col_b:
                if st.button("🗑️ Remove", key=f"del_{i}", use_container_width=True):
                    st.session_state.medications.pop(i)
                    st.session_state.taken_today.pop(i, None)
                    st.rerun()
    else:
        st.info("No medications yet. Add one above to get started!")

with right:
    st.markdown("### 📊 Why HealthTrack?")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="metric-card"><small>Users</small><h2>10K+</h2><small>↗️ 📈</small></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="metric-card"><small>Health Score</small><h2>98%</h2><small>↗️ 💚</small></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="metric-card"><small>Rating</small><h2>4.9 ⭐</h2><small>↗️ 🔥</small></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Live adherence
    total_meds = len(st.session_state.medications)
    taken_count = len(st.session_state.taken_today)
    if total_meds > 0:
        adherence = int((taken_count / total_meds) * 100) if total_meds else 0
        st.markdown("### 🎯 Today's Adherence")
        st.progress(adherence / 100)
        st.markdown(f"**{taken_count}/{total_meds} medications taken — {adherence}%**")
        if adherence == 100:
            st.balloons()
            st.success("Perfect! You took all your meds today! 🎉🔥")
    else:
        st.markdown("### ✨ How it works")
        st.write("1. Create your account\n2. Add your medications\n3. Track daily intake\n4. Build healthy streaks!")
        st.markdown("---")
        st.markdown("### 🔔 Coming Soon")
        st.write("💰 Health Finance Tracker\n📈 Live Vitals Monitor\n💧 Water & Sleep Tracker")

st.markdown("<br><hr><center><small>Built with 💜 by Anita Asuambuk | HealthTrack Pro v2.0 | 2026</small></center>", unsafe_allow_html=True)
