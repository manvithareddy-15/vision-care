import streamlit as st
from datetime import date, datetime
import uuid

# Initialize session state if needed
if "appointments" not in st.session_state:
    st.session_state.appointments = []

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="Doctor Appointment",
                   page_icon="👨‍⚕️", layout="centered")

# -------------------------------
# 🎨 CUSTOM CSS (YOUR THEME)
# -------------------------------
st.markdown("""
<style>
            /* Change ONLY red focus/border color to white */
:root {
    --primary-color: #E8EEF9 !important;
}

/* Replace red border when focused */
.stSelectbox div[data-baseweb="select"]:focus-within,
input:focus,
textarea:focus {
    border-color: #E8EEF9 !important;
}

/* Replace red focus ring */
.stSelectbox div[data-baseweb="select"]:focus-within,
input:focus,
textarea:focus {
    box-shadow: 0 0 0 1px #E8EEF9 !important;
}

.stApp {
    background: linear-gradient(135deg, #0B1220 0%, #0D1B2A 100%);
    color: #E8EEF9;
}

/* TITLE */
.main-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #80C6FF;
    text-align: center;
    margin-bottom: 0.2rem;
}

.subtitle {
    color: #AFC4DE;
    text-align: center;
    margin-bottom: 1.5rem;
}

/* CARD */
.card {
    background: rgba(17, 26, 41, 0.85);
    border: 1px solid #1E3A5F;
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 20px rgba(0,0,0,0.35);
}

/* SECTION TITLE */
.section-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #7CC4FF;
    margin-bottom: 0.6rem;
}

/* INPUTS */
input, textarea, select {
    background-color: #0D1B2A !important;
    color: #E8EEF9 !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 8px !important;
}

/* BUTTON */
.stButton>button {
    background: #4AA9FF;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 0.5rem 1rem;
}

.stButton>button:hover {
    background: #7CC4FF;
    color: black;
}

/* TIP BOX */
.tip {
    background: rgba(13, 88, 173, 0.18);
    border-left: 4px solid #4AA9FF;
    padding: 0.6rem;
    border-radius: 10px;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("""
<div class="main-title">👨‍⚕️ Vision Eye Care</div>
<div class="subtitle">Book an appointment with an eye specialist in Hyderabad</div>
""", unsafe_allow_html=True)

current_patient_username = st.session_state.get("username", "")
current_patient_name = st.session_state.get("patients", {}).get(
    current_patient_username, {}).get("name", "")

accepted_appointments = [
    apt for apt in st.session_state.appointments
    if apt.get("status") == "accepted" and (
        (current_patient_username and apt.get("patient_username") == current_patient_username) or
        (current_patient_name and apt.get("patient_name") == current_patient_name)
    )
]

if accepted_appointments:
    st.success(
        f"🎉 You have {len(accepted_appointments)} confirmed appointment(s).")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">✅ Your Confirmed Appointments</div>',
                unsafe_allow_html=True)
    for apt in accepted_appointments:
        st.markdown(f"""
            <div style='padding: 14px 0; border-bottom: 1px solid #1E3A5F;'>
                <strong>Hospital:</strong> {apt['hospital']}<br>
                <strong>Doctor:</strong> {apt['doctor']}<br>
                <strong>Date:</strong> {apt['date']} at {apt['time']}<br>
                <strong>Reason:</strong> {apt['reason']}<br>
                <strong>Confirmed on:</strong> {apt.get('confirmed_date', 'N/A')}
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("No confirmed appointments yet. Book one and wait for doctor confirmation.")

# -------------------------------
# DATA
# -------------------------------
hyderabad_data = {
    "Apollo Eye Hospital": [
        "Dr. Priya Sharma - Eye Specialist",
        "Dr. Rahul Verma - Retina Specialist"
    ],
    "LV Prasad Eye Institute": [
        "Dr. Kavya Reddy - Cornea Specialist",
        "Dr. Ramesh Kumar - Pediatric Eye Specialist"
    ],
    "Care Hospital": [
        "Dr. Nisha Patel - General Ophthalmologist",
        "Dr. Arjun Reddy - Cataract Specialist"
    ],
    "Maxivision Eye Hospital": [
        "Dr. Anil Kumar - Cataract Specialist",
        "Dr. Sneha Gupta - LASIK Specialist"
    ],
    "Centre for Sight": [
        "Dr. Meena Gupta - LASIK Specialist",
        "Dr. Rohit Sharma - Retina Specialist"
    ],
    "Dr. Agarwal’s Eye Hospital": [
        "Dr. Suresh Babu - Retina Specialist",
        "Dr. Kavitha Rao - Eye Surgeon"
    ],
    "Medivision Eye & Health Care": [
        "Dr. Swathi Reddy - Eye Specialist",
        "Dr. Mahesh Babu - General Ophthalmologist"
    ],
    "Win Vision Eye Hospitals": [
        "Dr. Kiran Kumar - Glaucoma Specialist",
        "Dr. Divya Nair - Cornea Specialist"
    ],
    "Eye Care Hospital (Secunderabad)": [
        "Dr. Rajesh - Ophthalmologist",
        "Dr. Pooja Sharma - Pediatric Eye Specialist"
    ],
    "Sankara Eye Hospital": [
        "Dr. Harish - Cataract Specialist",
        "Dr. Lakshmi Devi - Retina Specialist"
    ],
    "Ojas Eye Hospital": [
        "Dr. Deepa - Pediatric Eye Specialist",
        "Dr. Naveen Kumar - Eye Surgeon"
    ],
    "Shreya Eye Care Centre": [
        "Dr. Mahesh - General Ophthalmologist",
        "Dr. Anusha Reddy - LASIK Specialist"
    ]
}

# -------------------------------
# FORM CARD
# -------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown('<div class="section-title">📍 Appointment Details</div>',
            unsafe_allow_html=True)

st.write("City: Hyderabad")

hospital = st.selectbox("Select Hospital", list(hyderabad_data.keys()))
doctor = st.selectbox("Select Doctor", hyderabad_data[hospital])

time_slots = ["9:00 AM", "10:30 AM", "12:00 PM", "2:00 PM", "4:00 PM"]

appointment_date = st.date_input(
    "Choose Appointment Date",
    min_value=date.today()
)

appointment_time = st.selectbox("Choose Time Slot", time_slots)

patient_name = st.text_input("Patient Name")
phone = st.text_input("Phone Number")
problem = st.text_area("Describe Your Eye Problem")

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# BOOK BUTTON
# -------------------------------
if st.button("Book Appointment"):
    if patient_name.strip() == "" or phone.strip() == "":
        st.error("Please enter patient name and phone number.")
    else:
        # Create appointment object with all required fields
        appointment = {
            "id": str(uuid.uuid4()),
            "patient_username": current_patient_username,
            "patient_name": patient_name,
            "phone": phone,
            "hospital": hospital,
            "doctor": doctor,
            "date": str(appointment_date),
            "time": appointment_time,
            "reason": problem if problem.strip() else "Eye Checkup",
            "status": "pending",
            "requested_date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        # Add to session state
        st.session_state.appointments.append(appointment)

        st.success("✅ Appointment Booked Successfully!")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title">📋 Appointment Summary</div>', unsafe_allow_html=True)

        st.write("👤 Patient:", patient_name)
        st.write("📍 City: Hyderabad")
        st.write("🏥 Hospital:", hospital)
        st.write("👨‍⚕️ Doctor:", doctor)
        st.write("📅 Date:", appointment_date)
        st.write("⏰ Time:", appointment_time)
        st.write("📞 Phone:", phone)

        if problem.strip():
            st.write("📝 Problem:", problem)

        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# TIPS SECTION
# -------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">💡 Tips Before Visit</div>',
            unsafe_allow_html=True)

tips = [
    "Carry previous prescriptions",
    "Avoid eye makeup before checkup",
    "Bring sunglasses if sensitive to light",
    "Note down your symptoms clearly"
]

for tip in tips:
    st.markdown(f'<div class="tip">✅ {tip}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Back to Dashboard
st.markdown("---")
if st.button("← Back to Dashboard", use_container_width=True):
    st.switch_page("LOGIN")
