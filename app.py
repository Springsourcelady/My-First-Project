import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="HealthTrack Pro", page_icon="💚", layout="wide")

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        padding: 2.5rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;
    }
    .med-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0; padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem;
    }
    .metric-card {
        background: white; padding: 1.2rem; border-radius: 12px; border: 1px solid #e5e7eb; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

if 'medications' not in st.session_state:
    st.session_state.medications = []
if 'taken_today' not in st.session_state:
    st.session_state.taken_today = {}

st.markdown("""
<div class="main-header">
    <h1>💚 HealthTrack Pro</h1>
    <p>Your Personal Wellness Journey, Beautifully Tracked ✨</p>
    <p style="font-size:0.9rem; margin-top:1rem;">Built with 💜 by Anita Asuambuk</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.2, 1])
with left:
    st.markdown("### 💊 Medication Reminder Center")
    with st.form("med_form"):
        med_name = st.text_input("Medication Name", placeholder="e.g. Vitamin C")
        dosage = st.text_input("Dosage", placeholder="e.g. 500mg")
        med_time = st.time_input("Daily Time", value=datetime.now().time())
        frequency = st.selectbox("Frequency", ["Daily", "Twice a day", "Weekly", "As needed"])
        add_med = st.form_submit_button("➕ Add Medication", use_container_width=True)
        if add_med and med_name:
            st.session_state.medications.append({"name": med_name, "dosage": dosage, "time": med_time.strftime("%H:%M"), "frequency": frequency})
            st.rerun()

    if st.session_state.medications:
        for i, med in enumerate(st.session_state.medications):
            st.markdown(f'<div class="med-card"><b>💊 {med["name"]}</b> - {med["dosage"]}<br>⏰ {med["time"]} | 🔁 {med["frequency"]}</div>', unsafe_allow_html=True)
            c1,c2 = st.columns(2)
            with c1:
                if st.button("✅ Taken Today", key=f"t_{i}", use_container_width=True):
                    st.session_state.taken_today[i]=True
                    st.rerun()
            with c2:
                if st.button("🗑️ Remove", key=f"d_{i}", use_container_width=True):
                    st.session_state.medications.pop(i)
                    st.rerun()

with right:
    st.markdown("### 📊 Why HealthTrack?")
    c1,c2,c3 = st.columns(3)
    with c1: st.markdown('<div class="metric-card"><small>Users</small><h2>10K+</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown('<div class="metric-card"><small>Health Score</small><h2>98%</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="metric-card"><small>Rating</small><h2>4.9 ⭐</h2></div>', unsafe_allow_html=True)
    if st.session_state.medications:
        adherence = int((len(st.session_state.taken_today)/len(st.session_state.medications))*100)
        st.markdown("### 🎯 Today's Adherence")
        st.progress(adherence/100)
        st.write(f"{len(st.session_state.taken_today)}/{len(st.session_state.medications)} taken — {adherence}%")
