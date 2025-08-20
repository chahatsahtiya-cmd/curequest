import streamlit as st
import datetime

# ================== Page Config ==================
st.set_page_config(
    page_title="EpidemicCare AI",
    page_icon="🩺",
    layout="wide"
)

# ================== Custom CSS ==================
st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #f0f9ff, #e8f5e9);
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
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #ff9800;
        color: #e65100;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ================== Session State ==================
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "last_reminder" not in st.session_state:
    st.session_state.last_reminder = None

# ================== Daily Reminder ==================
def show_daily_reminder():
    today = datetime.date.today()
    if st.session_state.last_reminder != today:
        st.session_state.last_reminder = today
        st.sidebar.markdown(
            "<div class='reminder'>🔔 Daily Reminder: Please check your health with EpidemicCare AI today!</div>",
            unsafe_allow_html=True
        )

# ================== Welcome Page ==================
def show_welcome():
    st.markdown("<h1 style='text-align:center; color:#2e7d32;'>🌍 Welcome to EpidemicCare AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px;'>Your trusted AI-powered health assistant for epidemic disease guidance.</p>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/3781/3781900.png", width=150)
    st.markdown("<p style='text-align:center;'>Click below to start your consultation.</p>", unsafe_allow_html=True)
    if st.button("🚀 Start Consultation"):
        st.session_state.page = "consultation"
        st.rerun()

# ================== Router ==================
show_daily_reminder()

if st.session_state.page == "welcome":
    show_welcome()
elif st.session_state.page == "consultation":
    # 🔹 PLACE YOUR WORKING AI DOCTOR CODE HERE 🔹
    # (Don’t change it — just paste it inside this block)
    pass
