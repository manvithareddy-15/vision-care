import streamlit as st
from openai import OpenAI   # if you're using it
from PIL import Image      # if needed


import json
import base64
import hashlib
import time
from datetime import date
from io import BytesIO
import streamlit as st
from PIL import Image
eye_knowledge = {
    "dryness": {
        "explanation": "The eye shows redness and irritation, which are common signs of dryness caused by lack of moisture.",
        "causes": "Prolonged screen time, dehydration, lack of sleep, exposure to AC or dust.",
        "good_news": "This is usually not serious and can be treated easily.",
        "warning_signs": "If redness increases or pain starts, consult a doctor.",
        "what_to_do": "Take breaks, drink water, reduce screen time, and use eye drops."
    },

    "infection": {
        "explanation": "Swelling, redness, or discharge may indicate an eye infection.",
        "causes": "Bacteria, viruses, or touching eyes with unclean hands.",
        "good_news": "Most infections are treatable with proper care.",
        "warning_signs": "Severe pain, yellow discharge, or vision issues.",
        "what_to_do": "Avoid touching eyes and consult a doctor."
    },

    "allergy": {
        "explanation": "Redness and itching suggest an allergic reaction.",
        "causes": "Dust, pollen, pollution, or cosmetics.",
        "good_news": "Usually temporary and manageable.",
        "warning_signs": "Persistent itching or swelling.",
        "what_to_do": "Avoid allergens and use prescribed drops."
    },

    "redness": {
        "explanation": "Redness may indicate irritation, dryness, or a mild infection.",
        "causes": "Eye strain, allergies, dry air, or minor irritation.",
        "good_news": "Many redness issues are temporary and improve with rest.",
        "warning_signs": "If redness worsens or is accompanied by pain, see a doctor.",
        "what_to_do": "Rest your eyes, use artificial tears, and avoid rubbing them."
    },

    "irritation": {
        "explanation": "Irritation often shows as discomfort and mild inflammation.",
        "causes": "Dust, smoke, dry air, or overuse of screens.",
        "good_news": "This is usually manageable with simple self-care.",
        "warning_signs": "Seek care if irritation persists or vision blurs.",
        "what_to_do": "Blink frequently, hydrate, and give your eyes a break."
    },

    "normal": {
        "explanation": "The eye appears healthy with no visible issues.",
        "causes": "—",
        "good_news": "Everything looks normal.",
        "warning_signs": "None",
        "what_to_do": "Maintain eye hygiene and regular checkups."
    }
}

st.markdown("""
        <div style="text-align: center; margin-top: -10px;">
        <div class="main-title">👁️ VisionCare AI</div>
        <div class="subtitle">AI-powered eye care assistant for quick self-checks</div>
        </div>
    """, unsafe_allow_html=True)
st.info("⚠️ This is not a medical diagnosis. Please consult a doctor if symptoms persist.")
st.set_page_config(page_title="VisionCare AI", page_icon="👁️", layout="wide")


def inject_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(135deg, #0B1220 0%, #0D1B2A 100%);
                color: #E8EEF9;
            }
            .main-title {
                font-size: 2.4rem;
                font-weight: 700;
                color: #80C6FF;
                text-align: center;      /* ✅ center */
                margin-top: -40px;       /* ✅ move UP */
                margin-bottom: 0.2rem;
            }
            .subtitle {
                color: #AFC4DE;
                text-align: center;      /* ✅ center */
                margin-bottom: 1rem;
            }
            
            .card {
                background: rgba(17, 26, 41, 0.85);
                border: 1px solid #1E3A5F;
                border-radius: 16px;
                padding: 1rem 1.2rem;
                margin-bottom: 1rem;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.35);
            }
            .section-title {
                font-size: 1.2rem;
                font-weight: 600;
                color: #7CC4FF;
                margin-bottom: 0.6rem;
            }
            .small-note {
                color: #9FB4CE;
                font-size: 0.9rem;
            }
            .tip {
                background: rgba(13, 88, 173, 0.18);
                border-left: 4px solid #4AA9FF;
                padding: 0.65rem 0.8rem;
                border-radius: 10px;
                margin-bottom: 0.5rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def card_start(title: str, emoji: str) -> None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-title">{emoji} {title}</div>', unsafe_allow_html=True
    )


def card_end() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def read_uploaded_or_captured_image(uploaded_file, camera_file):
    if uploaded_file is not None:
        return uploaded_file.read()
    if camera_file is not None:
        return camera_file.getvalue()
    return None


def analyze_eye_image(image_bytes: bytes):
    text = """You are a medical assistant AI.

Analyze this eye image carefully.

Return ONLY JSON with ALL these fields:

- condition
- severity (low, medium, high)
- message_type (info, warning, danger)
- message (short summary)
- confidence (0-100)

- explanation (what it is)
- causes (why it happens)
- good_news (if harmless)
- warning_signs (when to worry)
- what_to_do (steps to take)

IMPORTANT:
- DO NOT skip any field
- Always return all fields
- Keep it simple and clear
"""
    # Deterministic placeholder logic based on image hash.
    digest = hashlib.md5(image_bytes).hexdigest()
    value = int(digest[:8], 16) % 100

    if value < 20:
        condition = "redness"
        severity = "high"
        message_type = "error"
        message = "Possible **redness** detected. Please monitor closely."
    elif value < 45:
        condition = "dryness"
        severity = "medium"
        message_type = "warning"
        message = "Signs of **dryness** found. Hydration and rest are recommended."
    elif value < 70:
        condition = "irritation"
        severity = "medium"
        message_type = "info"
        message = "Mild **irritation** indicators observed."
    else:
        condition = "normal"
        severity = "low"
        message_type = "success"
        message = "Eye appears **normal** in this AI simulation."

    confidence = 65 + (int(digest[8:10], 16) % 31)  # 65-95
    knowledge = eye_knowledge.get(condition, eye_knowledge["normal"])
    return {
        "condition": condition,
        "severity": severity,
        "message_type": message_type,
        "message": message,
        "confidence": confidence,
        "explanation": knowledge["explanation"],
        "causes": knowledge["causes"],
        "good_news": knowledge["good_news"],
        "warning_signs": knowledge["warning_signs"],
        "what_to_do": knowledge["what_to_do"],
    }


def analyze_symptoms(symptoms: dict):
    score = sum(1 for selected in symptoms.values() if selected)

    if score == 0:
        return {
            "condition": "normal",
            "severity": "low",
            "message_type": "success",
            "message": "No major symptoms selected. Your eye condition looks stable.",
        }

    # Red flags carry extra weight.
    red_flag = symptoms["eye_pain"] or symptoms["blurred_vision"]
    if red_flag and score >= 2:
        return {
            "condition": "needs_attention",
            "severity": "high",
            "message_type": "error",
            "message": "Symptoms indicate possible strain or infection. Medical attention is advised.",
        }

    if score >= 2:
        return {
            "condition": "mild_issue",
            "severity": "medium",
            "message_type": "warning",
            "message": "Multiple symptoms detected. Consider lifestyle changes and monitoring.",
        }

    return {
        "condition": "minor",
        "severity": "low",
        "message_type": "info",
        "message": "A minor symptom is present. Keep observing for changes.",
    }


def show_message(message_type: str, message: str) -> None:
    if message_type == "error":
        st.error(message)
    elif message_type == "warning":
        st.warning(message)
    elif message_type == "info":
        st.info(message)
    else:
        st.success(message)


def combine_results(image_result, symptom_result):
    severity_rank = {"low": 1, "medium": 2, "high": 3}
    image_severity = severity_rank.get(
        image_result["severity"], 1) if image_result else 1
    symptom_severity = severity_rank.get(
        symptom_result["severity"], 1) if symptom_result else 1
    combined_level = max(image_severity, symptom_severity)

    if combined_level == 3:
        return {
            "status": "needs_attention",
            "message_type": "error",
            "message": "Combined analysis suggests your eye condition needs attention.",
            "doctor_needed": True,
        }
    if combined_level == 2:
        return {
            "status": "monitor",
            "message_type": "warning",
            "message": "Combined analysis suggests monitoring and preventive care.",
            "doctor_needed": False,
        }
    return {
        "status": "normal",
        "message_type": "success",
        "message": "Combined analysis appears normal.",
        "doctor_needed": False,
    }


def main():
    inject_styles()

    if "image_result" not in st.session_state:
        st.session_state.image_result = None
    if "symptom_result" not in st.session_state:
        st.session_state.symptom_result = None
    if "combined_result" not in st.session_state:
        st.session_state.combined_result = None

    left_col, right_col = st.columns([1.2, 1], gap="large")

    # 🔵 LEFT SIDE
    with left_col:

        # 📷 IMAGE ANALYSIS
        card_start("Image Upload & AI Analysis", "📷")

        uploaded_file = st.file_uploader(
            "Upload an eye image", type=["jpg", "jpeg", "png"])
        camera_file = st.camera_input("Or capture an image")

        image_bytes = read_uploaded_or_captured_image(
            uploaded_file, camera_file)

        if image_bytes:
            image = Image.open(BytesIO(image_bytes))
            st.image(image, caption="Selected Eye Image",
                     use_container_width=True)

            if st.button("Analyze Eye Image"):
                with st.spinner("Analyzing..."):
                    time.sleep(1.5)
                    st.session_state.image_result = analyze_eye_image(
                        image_bytes)

        if st.session_state.image_result:
            result = st.session_state.image_result

            show_message(result["message_type"], result["message"])

            st.markdown(f"### 🧠 Condition: {result['condition'].title()}")
            st.markdown(f"⚠️ Severity: {result['severity'].title()}")

            st.markdown(f"**AI Confidence Score:** {result['confidence']}%")
            st.progress(result["confidence"] / 100)

            # 👉 ADD FROM HERE ⬇️

            st.markdown(f"💡 **Explanation:** {result['explanation']}")
            st.markdown(f"📌 **Causes:** {result['causes']}")
            st.markdown(f"😊 **Good news:** {result['good_news']}")
            st.markdown(f"🚨 **Warning signs:** {result['warning_signs']}")
            st.markdown(f"👉 **What to do:** {result['what_to_do']}")

    card_end()

    # 🟢 RIGHT SIDE
    with right_col:
        # 🩺 SYMPTOMS
        card_start("Symptom Checker", "🩺")

        redness = st.checkbox("Eye Redness")
        eye_pain = st.checkbox("Eye Pain")
        blurred_vision = st.checkbox("Blurred Vision")
        dry_eyes = st.checkbox("Dry Eyes")

        if st.button("Check Symptoms"):
            symptoms = {
                "redness": redness,
                "eye_pain": eye_pain,
                "blurred_vision": blurred_vision,
                "dry_eyes": dry_eyes,
            }
            st.session_state.symptom_result = analyze_symptoms(symptoms)

        if st.session_state.symptom_result:
            show_message(
                st.session_state.symptom_result["message_type"],
                st.session_state.symptom_result["message"],
            )

            card_end()

        # 🤖 COMBINED RESULT
        card_start("Final Result", "🤖")

        if st.button("Generate Final Result"):
            st.session_state.combined_result = combine_results(
                st.session_state.image_result,
                st.session_state.symptom_result,
            )

        if st.session_state.combined_result:
            result = st.session_state.combined_result
            show_message(result["message_type"], result["message"])
        else:
            st.info("Run analysis to see final result")

        card_end()

        # 💡 TIPS
        card_start("Eye Care Tips", "💡")

        tips = [
            "Follow the 20-20-20 rule.",
            "Stay hydrated.",
            "Avoid rubbing eyes.",
            "Use proper lighting.",
            "Do regular eye checkups.",
        ]

        for tip in tips:
            st.markdown(
                f'<div class="tip">✅ {tip}</div>', unsafe_allow_html=True)

        card_end()

        if st.button("Check Result"):
            symptom_payload = {
                "redness": redness,
                "eye_pain": eye_pain,
                "blurred_vision": blurred_vision,
                "dry_eyes": dry_eyes,
            }
            st.session_state.symptom_result = analyze_symptoms(symptom_payload)

        if st.session_state.symptom_result:
            show_message(
                st.session_state.symptom_result["message_type"],
                st.session_state.symptom_result["message"],
            )
        card_end()


if __name__ == "__main__":
    main()
