 # Copyright (c) 2026 Anita Asuambuk. All Rights Reserved
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="HealthTrack", page_icon="💚", layout="centered")
st.title("💚 HealthTrack - Your Health, Tracked")
st.write("Built by Anita Asuambuk")

menu = st.sidebar.selectbox("Menu", ["Sign Up", "Dashboard", "Add Health Data"])

if menu == "Sign Up":
    st.header("Create Your Account")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    age = st.number_input("Age", 10, 100, 25)
    gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    if st.button("Create Account"):
        st.success(f"Welcome {name}! Account created.")
        st.balloons()

elif menu == "Dashboard":
    st.header("Your Progress - 7 Days")
    dates = ["10-13", "10-14", "10-15", "10-16", "10-17", "10-18", "10-19"]
    weight = [78.0, 77.8, 77.5, 77.3, 77.0, 76.8, 76.5]
    hr = [80, 78, 82, 75, 76, 74, 73]
    bp_sys = [130, 128, 125, 124, 122, 120, 118]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Weight Loss", "1.5kg", "-1.9%")
    with col2:
        st.metric("Heart Rate", "73 bpm", "-7 bpm")

    fig, ax = plt.subplots()
    ax.plot(dates, weight, marker='o', color='green')
    ax.set_title("Weight Trend")
    ax.set_ylabel("kg")
    st.pyplot(fig)
    st.success("Insight: Weight decreasing, BP improving 130->118!")

elif menu == "Add Health Data":
    st.header("Today's Check-in")
    w = st.number_input("Weight (kg)", 40.0, 200.0, 76.5)
    s = st.number_input("Steps", 0, 30000, 5000)
    if st.button("Save My Data"):
        st.success("Data saved! Dashboard updated.")

print("app.py file created successfully!")
