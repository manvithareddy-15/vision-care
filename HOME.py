import streamlit as st


# IMPORT YOUR PATIENT FILE HERE
import patient_file  # Replace 'patient_file' with your actual filename
# Or if it's a specific function: from patient_file import function_name

# Page config
st.set_page_config(
    page_title="VisionCare AI",
    page_icon="👁️",
    layout="centered"
)


# PAGE CONFIG
st.set_page_config(page_title="Home", page_icon="👁️", layout="centered")

# UI
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #1e3a8a, #38bdf8);
    color: white;
}
h1 {
    text-align: center;
}
.card {
    background-color: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin: 15px 0;
}
</style>
""", unsafe_allow_html=True)

st.title(" VisionCare AI Dashboard")
st.markdown("### Choose a service 👇")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("👁️ Eye Analysis")
    if st.button("Analyse my Eye"):
        st.switch_page("pages/EYE_ANALYSIS.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("👨‍⚕️ Doctor Appointment")
    if st.button("Book Appointment"):
        st.switch_page("pages/DOCTOR_APPOINTMENT.py")
    st.markdown('</div>', unsafe_allow_html=True)

# Logout
st.markdown("---")
