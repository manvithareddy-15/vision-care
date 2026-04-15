import streamlit as st
from datetime import datetime, timedelta
import uuid

# Page config
st.set_page_config(
    page_title="VisionCare AI",
    page_icon="👁️",
    layout="centered"
)

# ── session state ─────────────────────────────────────────────
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "login"
if "selected_patient" not in st.session_state:
    st.session_state.selected_patient = None
if "appointments" not in st.session_state:
    st.session_state.appointments = []  # List of appointment requests
if "patients" not in st.session_state:
    st.session_state.patients = {
        "patient1": {"name": "John Doe", "email": "john@example.com", "phone": "+1234567890"},
        "admin": {"name": "Admin User", "email": "admin@example.com", "phone": "+1234567890"}
    }

# ── mock credentials ───────────────────────────────────────────
PATIENT_CREDENTIALS = {"admin": "password", "patient1": "pass123"}
DOCTOR_CREDENTIALS = {"dr.smith": "doctor123", "dr.jones": "secure456"}

# ══════════════════════════════════════════════════════════════
#  GLOBAL CSS
# ══════════════════════════════════════════════════════════════
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
    font-family: 'Inter', sans-serif;
}
[data-testid="stHeader"]  { background-color: #0d1117 !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stSidebar"] { display: none; }
.block-container          { padding-top: 2rem; max-width: 860px; }

/* ── top bar ── */
.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 0 24px 0; border-bottom: 1px solid #21262d; margin-bottom: 32px;
}
.brand            { font-size: 18px; font-weight: 700; letter-spacing: 0.5px; color: #e6edf3; }
.brand span       { color: #4fc3f7; }
.page-label       { font-size: 11px; color: #8b949e; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 32px; }
.dots             { display: flex; gap: 6px; align-items: center; }
.dot              { width: 10px; height: 10px; border-radius: 50%; background: #30363d; }
.dot.active       { background: #4fc3f7; width: 24px; border-radius: 5px; }

/* ── titles ── */
.login-title    { font-size: 32px; font-weight: 700; text-align: center; color: #e6edf3; margin-bottom: 6px; }
.login-subtitle { font-size: 14px; color: #8b949e; text-align: center; margin-bottom: 32px; }

/* ── card ── */
.login-card { background: #161b22; border: 1px solid #21262d; border-radius: 12px; padding: 32px 32px 28px 32px; }

/* ── inputs ── */
[data-testid="stTextInput"] input {
    background-color: #0d1117 !important; border: 1px solid #30363d !important;
    border-radius: 8px !important; color: #e6edf3 !important;
    padding: 12px 16px !important; font-size: 14px !important; font-family: 'Inter', sans-serif !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #4fc3f7 !important; box-shadow: 0 0 0 2px rgba(79,195,247,.15) !important; outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: #484f58 !important; }
[data-testid="stTextInput"] label {
    font-size: 11px !important; font-weight: 600 !important;
    letter-spacing: 1.5px !important; text-transform: uppercase !important; color: #8b949e !important;
}

/* ── button ── */
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #1a6fa5, #4fc3f7) !important;
    color: #fff !important; border: none !important; border-radius: 8px !important;
    padding: 12px !important; font-size: 15px !important; font-weight: 600 !important;
    width: 100% !important; cursor: pointer !important; transition: all 0.2s ease !important;
    letter-spacing: 0.5px !important; margin-top: 8px !important;
}
[data-testid="stButton"] button:hover {
    opacity: .9 !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(79,195,247,.3) !important;
}

/* ── tab bar ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #161b22 !important; border-radius: 10px 10px 0 0; border-bottom: 1px solid #21262d;
    gap: 0;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important; color: #8b949e !important;
    font-size: 13px !important; font-weight: 600 !important; letter-spacing: 1px;
    text-transform: uppercase; padding: 14px 32px !important; border: none !important;
    border-bottom: 2px solid transparent !important; border-radius: 0 !important;
    transition: all .2s;
}
[data-testid="stTabs"] [aria-selected="true"] {
    color: #4fc3f7 !important; border-bottom: 2px solid #4fc3f7 !important;
}
[data-testid="stTabs"] [data-baseweb="tab-panel"] {
    background: #161b22 !important; border: 1px solid #21262d !important;
    border-top: none !important; border-radius: 0 0 12px 12px; padding: 28px 32px !important;
}

/* ── doctor accent ── */
.icon-circle {
    width: 64px; height: 64px; border-radius: 50%;
    background: linear-gradient(145deg, #1c3d52, #0d5a7a); border: 1px solid #4fc3f7;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 24px auto; font-size: 26px;
    box-shadow: 0 0 20px rgba(79,195,247,.15);
}

.doctor-icon-circle {
    width: 64px; height: 64px; border-radius: 50%;
    background: linear-gradient(145deg, #1c2333, #1a2e1c); border: 1px solid #2ea043;
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 24px auto; font-size: 26px;
    box-shadow: 0 0 20px rgba(86,211,100,.15);
}

/* ── dashboard ── */
.dash-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 0 20px; border-bottom: 1px solid #21262d; margin-bottom: 28px;
}
.dash-title   { font-size: 22px; font-weight: 700; color: #e6edf3; }
.dash-badge   {
    font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;
    padding: 4px 12px; border-radius: 20px;
}
.badge-patient { background: rgba(79,195,247,.15); color: #4fc3f7; border: 1px solid rgba(79,195,247,.3); }
.badge-doctor  { background: rgba(86,211,100,.15); color: #56d364; border: 1px solid rgba(86,211,100,.3); }

.card {
    background-color: rgba(255,255,255,0.1);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin: 15px 0;
    transition: all 0.3s ease;
}
.card:hover {
    transform: translateY(-5px);
    background-color: rgba(255,255,255,0.15);
}

.stat-card {
    background: #161b22; border: 1px solid #21262d; border-radius: 10px; padding: 20px;
    text-align: center; margin-bottom: 16px;
}
.stat-num  { font-size: 28px; font-weight: 700; }
.stat-lbl  { font-size: 12px; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px; }
.stat-blue { color: #4fc3f7; }
.stat-green{ color: #56d364; }
.stat-red  { color: #f85149; }

.info-block {
    background: #161b22; border: 1px solid #21262d; border-radius: 10px; padding: 20px 24px; margin-bottom: 16px;
}
.info-block h4 { font-size: 13px; color: #8b949e; letter-spacing: 1px; text-transform: uppercase; margin: 0 0 12px; }
.info-row  { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #21262d; font-size: 14px; }
.info-row:last-child { border-bottom: none; }
.info-key  { color: #8b949e; }
.info-val  { color: #e6edf3; font-weight: 500; }

.appointment-card {
    background: #1a1f2e;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
    transition: all 0.2s ease;
}
.appointment-card:hover {
    border-color: #4fc3f7;
    transform: translateX(4px);
}
.appointment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}
.appointment-patient {
    font-weight: 700;
    font-size: 16px;
    color: #4fc3f7;
}
.appointment-date {
    font-size: 12px;
    color: #8b949e;
}
.appointment-details {
    font-size: 13px;
    color: #e6edf3;
    margin-bottom: 12px;
}
.appointment-reason {
    background: #0d1117;
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 13px;
    margin-bottom: 12px;
    border-left: 3px solid #4fc3f7;
}
.status-pending {
    color: #e3b341;
    font-size: 12px;
    font-weight: 600;
}
.status-accepted {
    color: #56d364;
    font-size: 12px;
    font-weight: 600;
}
.status-declined {
    color: #f85149;
    font-size: 12px;
    font-weight: 600;
}
.empty-state {
    text-align: center;
    padding: 40px;
    color: #8b949e;
}
.empty-state-icon {
    font-size: 48px;
    margin-bottom: 16px;
}
.button-group {
    display: flex;
    gap: 10px;
    margin-top: 12px;
}
.accept-btn {
    background: linear-gradient(135deg, #238636, #2ea043) !important;
}
.decline-btn {
    background: linear-gradient(135deg, #da3633, #f85149) !important;
}

.logout-wrap { text-align: right; margin-top: 32px; }

hr { border-color: #21262d !important; }

/* Textarea styling */
[data-testid="stTextArea"] textarea {
    background-color: #0d1117 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Form styling */
[data-testid="stForm"] {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 20px;
}
</style>
"""


def topbar(page_num: int, label: str):
    dots_html = "".join(
        f'<div class="dot{" active" if i == page_num else ""}"></div>'
        for i in range(1, 4)
    )
    st.markdown(f"""
    <div class="topbar">
        <div class="brand">Vision<span>Care</span> AI</div>
        <div class="dots">{dots_html}</div>
    </div>
    <div class="page-label">{label}</div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  LOGIN PAGE
# ══════════════════════════════════════════════════════════════
def render_login():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    topbar(1, "Page 1 — Login")

    tab_patient, tab_doctor = st.tabs(["🧑‍💼  Patient", "🩺  Doctor"])

    # ── Patient tab ───────────────────────────────────────────
    with tab_patient:
        st.markdown("""
        <div class="icon-circle">👁️</div>
        <div class="login-title">Welcome back</div>
        <div class="login-subtitle">Sign in to your <b>Patient</b> account</div>
        """, unsafe_allow_html=True)

        p_user = st.text_input(
            "USERNAME", placeholder="Enter your username", key="p_user")
        p_pass = st.text_input(
            "PASSWORD", placeholder="••••••••", type="password", key="p_pass")

        if st.button("Login as Patient", key="btn_patient"):
            if not p_user or not p_pass:
                st.error("Please enter both username and password.")
            elif PATIENT_CREDENTIALS.get(p_user) == p_pass:
                st.session_state.role = "patient"
                st.session_state.username = p_user
                st.session_state.page = "patient_dashboard"
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")

    # ── Doctor tab ────────────────────────────────────────────
    with tab_doctor:
        st.markdown("""
        <div class="doctor-icon-circle">🩺</div>
        <div class="login-title">Doctor Portal</div>
        <div class="login-subtitle">Sign in to your <b style="color:#56d364">Doctor</b> account</div>
        """, unsafe_allow_html=True)

        d_user = st.text_input(
            "DOCTOR USERNAME", placeholder="e.g. dr.smith", key="d_user")
        d_pass = st.text_input(
            "PASSWORD", placeholder="••••••••", type="password", key="d_pass")

        if st.button("Login as Doctor", key="btn_doctor"):
            if not d_user or not d_pass:
                st.error("Please enter both username and password.")
            elif DOCTOR_CREDENTIALS.get(d_user) == d_pass:
                st.session_state.role = "doctor"
                st.session_state.username = d_user
                st.session_state.page = "doctor_dashboard"
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")


# ══════════════════════════════════════════════════════════════
#  PATIENT DASHBOARD (with appointment booking)
# ══════════════════════════════════════════════════════════════
def render_patient_dashboard():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    topbar(1, "Page 1 — Patient Dashboard")

    accepted_for_patient = [
        apt for apt in st.session_state.appointments
        if apt.get("status") == "accepted" and apt.get("patient_username") == st.session_state.get("username", "")
    ]
    if accepted_for_patient:
        st.success(
            f"🎉 You have {len(accepted_for_patient)} confirmed appointment(s). Check 'Doctor Appointment' to view details.")

    st.markdown(f"""
    <div class="dash-header">
        <div class="dash-title">👁️ VisionCare AI Dashboard</div>
        <div class="dash-badge badge-patient">Patient</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Choose a service 👇")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <div style="font-size: 48px; margin-bottom: 16px;">👁️</div>
            <h3 style="margin: 0; color: #e6edf3;">Eye Analysis</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Eye Analysis", key="eye_analysis_btn", use_container_width=True):
            st.switch_page("pages/EYE_ANALYSIS.py")

    with col2:
        st.markdown("""
        <div class="card">
            <div style="font-size: 48px; margin-bottom: 16px;">👨‍⚕️</div>
            <h3 style="margin: 0; color: #e6edf3;">Doctor Appointment</h3>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Book Appointment", key="appointment_btn", use_container_width=True):
            st.switch_page("pages/DOCTOR_APPOINTMENT.py")

    st.markdown("---")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.role = None
            st.session_state.username = ""
            st.session_state.page = "login"
            st.rerun()

# ══════════════════════════════════════════════════════════════
#  DOCTOR DASHBOARD (with appointment management)
# ══════════════════════════════════════════════════════════════


def render_doctor_dashboard():
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
    topbar(2, "Page 2 — Doctor Dashboard")

    name = st.session_state.username.replace("dr.", "").capitalize()
    st.markdown(f"""
    <div class="dash-header">
        <div class="dash-title">🩺 Dr. {name}'s Portal</div>
        <div class="dash-badge badge-doctor">Doctor</div>
    </div>
    """, unsafe_allow_html=True)

    # Statistics
    pending_count = len(
        [apt for apt in st.session_state.appointments if apt["status"] == "pending"])
    accepted_count = len(
        [apt for apt in st.session_state.appointments if apt["status"] == "accepted"])
    total_count = len(st.session_state.appointments)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="stat-card"><div class="stat-num stat-green">{pending_count}</div><div class="stat-lbl">Pending Requests</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(
            f'<div class="stat-card"><div class="stat-num stat-green">{accepted_count}</div><div class="stat-lbl">Confirmed Appointments</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(
            f'<div class="stat-card"><div class="stat-num stat-green">{total_count}</div><div class="stat-lbl">Total Requests</div></div>', unsafe_allow_html=True)

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(
        ["📋 Pending Requests", "✅ Confirmed Appointments", "📊 Dashboard Overview"])

    # Tab 1: Pending Appointment Requests
    with tab1:
        pending_appointments = [
            apt for apt in st.session_state.appointments if apt["status"] == "pending"]

        if not pending_appointments:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">🎉</div>
                <div>No pending appointment requests!</div>
                <div style="font-size: 12px; margin-top: 8px;">All caught up for now.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for apt in pending_appointments:
                with st.container():
                    st.markdown(f"""
                    <div class="appointment-card">
                        <div class="appointment-header">
                            <div class="appointment-patient">👤 {apt['patient_name']}</div>
                            <div class="appointment-date">📅 Requested: {apt['requested_date']}</div>
                        </div>
                        <div class="appointment-details">
                            <strong>Preferred Date:</strong> {apt['date']} at {apt['time']}<br>
                            <strong>Doctor Selected:</strong> {apt['doctor']}
                        </div>
                        <div class="appointment-reason">
                            <strong>Reason for visit:</strong><br>
                            {apt['reason']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Accept", key=f"accept_{apt['id']}", use_container_width=True):
                            for appointment in st.session_state.appointments:
                                if appointment["id"] == apt["id"]:
                                    appointment["status"] = "accepted"
                                    appointment["confirmed_date"] = datetime.now().strftime(
                                        "%Y-%m-%d %H:%M")
                                    break
                            st.success(
                                f"✅ Appointment for {apt['patient_name']} has been accepted!")
                            st.rerun()

                    with col2:
                        if st.button("❌ Decline", key=f"decline_{apt['id']}", use_container_width=True):
                            for appointment in st.session_state.appointments:
                                if appointment["id"] == apt["id"]:
                                    appointment["status"] = "declined"
                                    break
                            st.warning(
                                f"❌ Appointment for {apt['patient_name']} has been declined.")
                            st.rerun()

                    st.markdown("<hr style='margin: 16px 0;'>",
                                unsafe_allow_html=True)

    # Tab 2: Confirmed Appointments
    with tab2:
        confirmed_appointments = [
            apt for apt in st.session_state.appointments if apt["status"] == "accepted"]

        if not confirmed_appointments:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-state-icon">📅</div>
                <div>No confirmed appointments yet.</div>
                <div style="font-size: 12px; margin-top: 8px;">Accept pending requests to see them here.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for apt in confirmed_appointments:
                st.markdown(f"""
                <div class="appointment-card">
                    <div class="appointment-header">
                        <div class="appointment-patient">👤 {apt['patient_name']}</div>
                        <div class="status-accepted">✅ Confirmed</div>
                    </div>
                    <div class="appointment-details">
                        <strong>📅 Date:</strong> {apt['date']} at {apt['time']}<br>
                        <strong>👨‍⚕️ Doctor:</strong> {apt['doctor']}<br>
                        <strong>📝 Reason:</strong> {apt['reason']}
                    </div>
                    <div style="font-size: 12px; color: #8b949e; margin-top: 8px;">
                        Confirmed on: {apt.get('confirmed_date', 'N/A')}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Tab 3: Dashboard Overview
    with tab3:
        total_appointments = len(st.session_state.appointments)
        acceptance_rate = int(len([a for a in st.session_state.appointments if a["status"]
                              == "accepted"]) / max(total_appointments, 1) * 100)

        st.markdown(f"""
        <div class="info-block">
            <h4>📊 Practice Statistics</h4>
            <div class="info-row"><span class="info-key">Total Appointment Requests</span><span class="info-val">{total_appointments}</span></div>
            <div class="info-row"><span class="info-key">Acceptance Rate</span><span class="info-val">{acceptance_rate}%</span></div>
            <div class="info-row"><span class="info-key">Most Common Reason</span><span class="info-val">Annual Check-up</span></div>
        </div>
        """, unsafe_allow_html=True)

        unique_patients = len(set([a["patient_name"]
                              for a in st.session_state.appointments]))

        st.markdown(f"""
        <div class="info-block">
            <h4>👥 Patient Demographics</h4>
            <div class="info-row"><span class="info-key">Total Patients</span><span class="info-val">{unique_patients}</span></div>
            <div class="info-row"><span class="info-key">New This Month</span><span class="info-val">3</span></div>
            <div class="info-row"><span class="info-key">Follow-ups Required</span><span class="info-val">2</span></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-block">
            <h4>⚠️ AI-Flagged Cases</h4>
            <div class="info-row"><span class="info-key">Patient #2041</span><span class="info-val" style="color:#f85149">⚠️ Suspected early glaucoma — review scan</span></div>
            <div class="info-row"><span class="info-key">Patient #1987</span><span class="info-val" style="color:#e3b341">🟡 Mild drusen deposits detected</span></div>
            <div class="info-row"><span class="info-key">Patient #2103</span><span class="info-val" style="color:#56d364">✅ Normal — no action required</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="logout-wrap">', unsafe_allow_html=True)
    if st.button("🚪 Logout", key="logout_doctor"):
        st.session_state.page = "login"
        st.session_state.role = None
        st.session_state.username = ""
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════
if st.session_state.page == "login":
    render_login()
elif st.session_state.page == "patient_dashboard":
    render_patient_dashboard()
elif st.session_state.page == "doctor_dashboard":
    render_doctor_dashboard()
