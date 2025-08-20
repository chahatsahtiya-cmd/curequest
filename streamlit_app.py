import streamlit as st
import pandas as pd
import datetime
import random
import tempfile
import os

# ================== Page Config ==================
st.set_page_config(
    page_title="EpidemicCare AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== Custom CSS ==================
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #e0f7fa, #e8f5e9);
    }
    .chat-bubble-doctor {
        background-color: #bbdefb;
        color: #0d47a1;
        padding: 12px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 80%;
    }
    .chat-bubble-user {
        background-color: #c8e6c9;
        color: #1b5e20;
        padding: 12px;
        border-radius: 15px;
        margin: 8px 0;
        max-width: 80%;
        margin-left: auto;
    }
    .reminder {
        background-color: #fff3e0;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #ff9800;
        color: #e65100;
        font-weight: bold;
        margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ================== Questions ==================
questions = [
    "What is your name?",
    "How old are you?",
    "Do you have any pre-existing medical conditions?",
    "Have you had a fever in the last 48 hours?",
    "Are you experiencing any cough or difficulty breathing?",
    "Do you have any body aches or joint pain?",
    "Have you noticed any loss of taste or smell?",
    "Are you experiencing fatigue or unusual tiredness?",
    "Any other symptoms you'd like to mention?"
]

# ================== Session State ==================
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "symptoms" not in st.session_state:
    st.session_state.symptoms = {}
if "last_reminder" not in st.session_state:
    st.session_state.last_reminder = None

# ================== AI Doctor Response ==================
def get_ai_response(step, user_input=None):
    responses = {
        0: "Hello! I'm Dr. AI, your medical assistant. What's your name?",
        1: f"Nice to meet you, {user_input}! How old are you?",
        2: "Do you have any pre-existing medical conditions?",
        3: "Have you had a fever in the last 48 hours?",
        4: "Are you experiencing any cough or difficulty breathing?",
        5: "Do you have any body aches or joint pain?",
        6: "Have you noticed any loss of taste or smell?",
        7: "Are you experiencing fatigue or unusual tiredness?",
        8: "Any other symptoms you'd like to mention?",
        9: "Thank you. I'm now analyzing your symptoms...",
        10: "Based on your symptoms, I'm developing a personalized treatment plan for you.",
        11: "I've prepared a comprehensive treatment plan. Let me walk you through it."
    }
    return responses.get(step, "Please tell me more about your health.")

# ================== Display Chat ==================
def display_chat():
    for sender, message in st.session_state.chat_history:
        if sender == "doctor":
            st.markdown(f"<div class='chat-bubble-doctor'>💙 Dr. AI: {message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble-user'>🧑 You: {message}</div>", unsafe_allow_html=True)

# ================== AI Doctor Page ==================
def show_ai_doctor():
    st.title("🩺 EpidemicCare AI Doctor")

    display_chat()

    if st.session_state.current_step < len(questions):
        current_question = get_ai_response(
            st.session_state.current_step, 
            st.session_state.symptoms.get("name")
        )

        # Add doctor question if not repeated
        if not st.session_state.chat_history or st.session_state.chat_history[-1][1] != current_question:
            st.session_state.chat_history.append(("doctor", current_question))

        # Handle inputs
        if st.session_state.current_step == 0:
            name = st.text_input("Your name")
            if st.button("Submit Name"):
                st.session_state.symptoms["name"] = name
                st.session_state.chat_history.append(("user", name))
                st.session_state.current_step += 1
                st.rerun()

        elif st.session_state.current_step == 1:
            age = st.number_input("Your age", min_value=0, max_value=120)
            if st.button("Submit Age"):
                st.session_state.symptoms["age"] = age
                st.session_state.chat_history.append(("user", str(age)))
                st.session_state.current_step += 1
                st.rerun()

        elif st.session_state.current_step == 2:
            conditions = st.text_input("Any pre-existing conditions?")
            if st.button("Submit Conditions"):
                st.session_state.symptoms["conditions"] = conditions
                st.session_state.chat_history.append(("user", conditions if conditions else "None"))
                st.session_state.current_step += 1
                st.rerun()
        else:
            options = ["Yes", "No", "Not sure"]
            response = st.radio("Choose:", options, key=f"q{st.session_state.current_step}")
            if st.button("Submit Answer", key=f"btn{st.session_state.current_step}"):
                st.session_state.symptoms[f"symptom_{st.session_state.current_step}"] = response
                st.session_state.chat_history.append(("user", response))
                st.session_state.current_step += 1
                st.rerun()
    else:
        st.success("✅ Consultation finished! AI Doctor will now analyze your symptoms.")
        st.write("👉 Your treatment plan will appear here soon.")

# ================== Welcome Page ==================
def show_welcome():
    st.markdown("<h1 style='text-align:center; color:#2e7d32;'>🌍 Welcome to EpidemicCare AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px;'>Your trusted AI-powered health assistant for epidemic disease guidance.</p>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3781/3781900.png", width=150)
    st.markdown("<p style='text-align:center;'>Click below to start your consultation.</p>", unsafe_allow_html=True)
    if st.button("🚀 Start Consultation"):
        st.session_state.page = "consultation"
        st.rerun()

# ================== Daily Reminder ==================
def show_daily_reminder():
    today = datetime.date.today()
    if st.session_state.last_reminder != today:
        st.session_state.last_reminder = today
        st.sidebar.markdown("<div class='reminder'>🔔 Don't forget to do your daily health check-in with EpidemicCare AI!</div>", unsafe_allow_html=True)

# ================== Router ==================
show_daily_reminder()

if st.session_state.page == "welcome":
    show_welcome()
elif st.session_state.page == "consultation":
    show_ai_doctor()
