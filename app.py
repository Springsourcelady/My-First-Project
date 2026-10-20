import streamlit as st
from datetime import datetime
import pandas as pd
import re

st.set_page_config(page_title="HealthTrack Pro - Green", page_icon="🌿", layout="wide")

# --- GREEN LOCAL THEME ---
st.markdown("""
<style>
    .stApp { background-color: #f6fef9; }
    .green-header {
        background: linear-gradient(135deg, #15803d 0%, #166534 50%, #14532d 100%);
        padding: 2.5rem 2rem; border-radius: 20px; color: white; text-align: center;
        box-shadow: 0 10px 25px rgba(21,128,61,0.3); margin-bottom: 2rem;
        border: 2px solid #bbf7d0;
    }
    .step-card {
        background: white; border-radius: 16px; padding: 1.8rem;
        border: 2px solid #dcfce7; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .progress-text { color: #15803d; font-weight: bold; text-align: center; }
    div.stButton > button:first-child {
        background: #15803d; color: white; border-radius: 10px; border: none;
        padding: 0.6rem; font-weight: bold;
    }
    div.stButton > button:first-child:hover { background: #166534; }
</style>
""", unsafe_allow_html=True)

# --- SESSION ---
defaults = {"step": 1, "medications": [], "taken": set(), "water": 0, "expenses": [], "logs": [], "profile": {}, "name": "", "dob_text": "", "phone": ""}
for k,v in defaults.items():
    if k not in st.session_state: st.session_state[k]=v

def parse_date(t):
    if not t: return None
    t=t.strip()
    for fmt in ["%d/%m/%Y","%d-%m-%Y","%d %m %Y","%m/%d/%Y","%Y-%m-%d","%d.%m.%Y"]:
        try: return datetime.strptime(t, fmt).date()
        except: continue
    if re.match(r"^\d{8}$", t):
        try: return datetime.strptime(t, "%d%m%Y").date()
        except: pass
    return None

# --- HEADER ---
st.markdown("""
<div class="green-header">
    <h1>🌿 HealthTrack Pro</h1>
    <p style="font-size:1.1rem; opacity:0.95;">Naija Green Wellness - Money • Water • Meds • Monitoring</p>
    <p>Built with 💜 by Anita Asuambuk • Village Green Edition</p>
</div>
""", unsafe_allow_html=True)

# --- PROGRESS ---
steps = {1:"👤 Name", 2:"📅 DOB", 3:"💊 Meds", 4:"💧 Water", 5:"💰 Money", 6:"📊 Dashboard"}
st.progress(st.session_state.step/6)
st.markdown(f'<p class="progress-text">Step {st.session_state.step} of 6: {steps[st.session_state.step]} — Click NEXT or SKIP</p>', unsafe_allow_html=True)

# --- NAVIGATION HELPERS ---
def next_step():
    st.session_state.step = min(6, st.session_state.step+1)
def prev_step():
    st.session_state.step = max(1, st.session_state.step-1)
def skip_step():
    next_step()

# --- STEP 1: NAME ---
if st.session_state.step == 1:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.subheader("👋 Step 1: Let's know you")
    st.write("This will personalize your health track.")
    name = st.text_input("Full Name *", value=st.session_state.name, placeholder="e.g. Anita Asuambuk")
    phone = st.text_input("Phone (optional)", value=st.session_state.phone, placeholder="080...")
    st.session_state.name = name
    st.session_state.phone = phone
    
    c1,c2 = st.columns(2)
    with c1: 
        if st.button("➡️ NEXT: Date of Birth", use_container_width=True, disabled=not name):
            st.session_state.profile["name"]=name
            next_step(); st.rerun()
    with c2:
        if st.button("⏭️ SKIP this", use_container_width=True):
            skip_step(); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- STEP 2: DOB - FAST TYPE ---
elif st.session_state.step == 2:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.subheader("📅 Step 2: Date of Birth")
    st.info("💡 JUST TYPE - No calendar scrolling! Example: 15/08/1995")
    dob_text = st.text_input("Type DOB here", value=st.session_state.dob_text, placeholder="DD/MM/YYYY - e.g. 15/08/1995")
    st.session_state.dob_text = dob_text
    parsed = parse_date(dob_text)
    if dob_text:
        if parsed: st.success(f"✅ Got it: {parsed.strftime('%d %B, %Y')} — You are {(datetime.now().date()-parsed).days//365} years old")
        else: st.error("❌ Use format 15/08/1995 or 15-08-1995")
    
    blood = st.selectbox("Blood Group (optional)", ["", "O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"])
    
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("⬅️ BACK", use_container_width=True):
            prev_step(); st.rerun()
    with c2:
        if st.button("➡️ NEXT: Medications", use_container_width=True):
            st.session_state.profile["dob"]=str(parsed) if parsed else ""
            st.session_state.profile["blood"]=blood
            next_step(); st.rerun()
    with c3:
        if st.button("⏭️ SKIP to Meds", use_container_width=True):
            skip_step(); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- STEP 3: MEDICATIONS ---
elif st.session_state.step == 3:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.subheader("💊 Step 3: Medication Reminders")
    with st.form("med", clear_on_submit=True):
        m1,m2 = st.columns(2)
        with m1: mn = st.text_input("Medication Name", placeholder="Vitamin C")
        with m2: ds = st.text_input("Dosage", placeholder="500mg")
        m3,m4 = st.columns(2)
        with m3: tm = st.text_input("Time (type!)", placeholder="08:00 or 8pm")
        with m4: fq = st.selectbox("Frequency", ["Daily","Twice daily","Weekly","As needed"])
        if st.form_submit_button("➕ Add Medication", use_container_width=True) and mn:
            st.session_state.medications.append({"name":mn,"dose":ds,"time":tm,"freq":fq})
            st.success(f"Added {mn}"); st.rerun()
    
    if st.session_state.medications:
        for i,med in enumerate(st.session_state.medications):
            done = i in st.session_state.taken
            c1,c2,c3 = st.columns([3,1,1])
            with c1: st.write(f"{'✅' if done else '💊'} **{med['name']}** - {med['dose']} @ {med['time']}")
            with c2:
                if st.button("Taken", key=f"t{i}", disabled=done):
                    st.session_state.taken.add(i); st.balloons(); st.rerun()
            with c3:
                if st.button("Del", key=f"d{i}"):
                    st.session_state.medications.pop(i); st.rerun()
    
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("⬅️ BACK", use_container_width=True): prev_step(); st.rerun()
    with c2:
        if st.button("➡️ NEXT: Water Tracking", use_container_width=True): next_step(); st.rerun()
    with c3:
        if st.button("⏭️ SKIP to Water", use_container_width=True): skip_step(); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- STEP 4: WATER ---
elif st.session_state.step == 4:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.subheader("💧 Step 4: Water Tracking")
    st.write("Tap quickly - no typing needed!")
    
    w1,w2,w3,w4 = st.columns(4)
    with w1:
        if st.button("🥤\n250ml", use_container_width=True): st.session_state.water+=250; st.rerun()
    with w2:
        if st.button("💧\n500ml", use_container_width=True): st.session_state.water+=500; st.rerun()
    with w3:
        if st.button("🧃\n1 Litre", use_container_width=True): st.session_state.water+=1000; st.rerun()
    with w4:
        if st.button("Reset", use_container_width=True): st.session_state.water=0; st.rerun()
    
    st.metric("Today", f"{st.session_state.water} ml", f"{st.session_state.water/2000*100:.0f}% of 2L")
    st.progress(min(st.session_state.water/2000,1.0))
    
    if st.session_state.water >= 2000:
        st.success("🎉 You reached your water goal! Well done!")
        st.balloons()
    
    st.divider()
    st.write("**Mood quick check:**")
    mood = st.select_slider("How you feel?", options=["😢 Low","😕 Tired","😐 Okay","🙂 Good","😄 Great"])
    if st.button("Save Mood"):
        st.session_state.logs.append({"time":datetime.now().strftime("%d/%m/%Y %H:%M"), "type":"Mood", "value":mood})
        st.success("Saved!")
    
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("⬅️ BACK", use_container_width=True): prev_step(); st.rerun()
    with c2:
        if st.button("➡️ NEXT: Money", use_container_width=True): next_step(); st.rerun()
    with c3:
        if st.button("⏭️ SKIP to Money", use_container_width=True): skip_step(); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- STEP 5: MONEY ---
elif st.session_state.step == 5:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.subheader("💰 Step 5: Financial Health Tracker")
    st.write("Track how much you spend on health - very important for Naija!")
    
    with st.form("money", clear_on_submit=True):
        c1,c2 = st.columns(2)
        with c1:
            d = st.text_input("Date - TYPE DD/MM/YYYY", placeholder="20/10/2026")
            cat = st.selectbox("Category", ["Medication","Doctor","Lab Test","Supplements","Food/Water","Transport to Hospital","Other"])
        with c2:
            amt = st.number_input("Amount ₦", min_value=0, step=500)
            desc = st.text_input("For what?", placeholder="Vitamin C for 1 month")
        if st.form_submit_button("💾 Save Expense") and amt>0:
            pd_date = parse_date(d)
            st.session_state.expenses.append({"date":d or datetime.now().strftime("%d/%m/%Y"), "cat":cat, "amt":amt, "desc":desc})
            st.success("Saved!"); st.rerun()
    
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.metric("Total Health Spend", f"₦{df['amt'].sum():,.0f}")
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df.groupby("cat")["amt"].sum())
    
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("⬅️ BACK", use_container_width=True): prev_step(); st.rerun()
    with c2:
        if st.button("➡️ FINISH: See Dashboard", use_container_width=True): next_step(); st.rerun()
    with c3:
        if st.button("⏭️ SKIP to Dashboard", use_container_width=True): skip_step(); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- STEP 6: DASHBOARD ---
else:
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.subheader(f"🌿 Welcome {st.session_state.name or 'Anita'}! Your Green Dashboard")
    
    k1,k2,k3,k4 = st.columns(4)
    with k1: st.metric("💊 Meds", f"{len(st.session_state.medications)}")
    with k2: st.metric("✅ Taken", f"{len(st.session_state.taken)}")
    with k3: st.metric("💧 Water", f"{st.session_state.water}ml")
    with k4: st.metric("💰 Spent", f"₦{sum([e['amt'] for e in st.session_state.expenses]):,.0f}" if st.session_state.expenses else "₦0")
    
    st.divider()
    c1,c2 = st.columns(2)
    with c1:
        st.write("**📝 Recent Health Logs**")
        if st.session_state.logs:
            for l in st.session_state.logs[-5:][::-1]:
                st.write(f"- {l['time']}: {l['type']} - {l['value']}")
        else:
            st.info("No logs yet")
    with c2:
        st.write("**💊 Adherence**")
        pct = int(len(st.session_state.taken)/len(st.session_state.medications)*100) if st.session_state.medications else 0
        st.progress(pct/100)
        st.write(f"{pct}% today")
    
    st.divider()
    b1,b2 = st.columns(2)
    with b1:
        if st.button("🔄 START OVER FROM STEP 1", use_container_width=True):
            st.session_state.step=1; st.rerun()
    with b2:
        if st.button("📥 Download My Data CSV", use_container_width=True):
            if st.session_state.expenses or st.session_state.logs:
                all_data = pd.DataFrame(st.session_state.expenses + st.session_state.logs)
                csv = all_data.to_csv(index=False).encode()
                st.download_button("Download Now", csv, "my_healthtrack_green.csv", "text/csv")
            else:
                st.warning("No data to download yet")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.success("🌿 This is your GREEN LOCAL LOOK - Fresh, natural, Naija style!")

# --- FOOTER NAV ---
st.markdown("---")
st.caption(f"Step {st.session_state.step}/6 • Use NEXT / BACK / SKIP to move between screens • All dates are TYPE-ABLE: DD/MM/YYYY")
