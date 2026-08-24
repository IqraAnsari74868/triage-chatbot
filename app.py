import streamlit as st
from symptom_extractor import extract_symptoms
from match_engine import match_conditions
from explainer import generate_explanation

st.set_page_config(page_title="Triage Chatbot", page_icon="🩺", layout="centered")

# ---------- Sidebar ----------
with st.sidebar:
    st.header("About this project")
    st.write(
        "A symptom-checker tool combining a **SQL database**, "
        "**Python matching logic**, and **LLM prompt engineering** "
        "to return possible conditions and urgency levels from "
        "free-text symptom descriptions."
    )
    st.markdown("---")
    st.caption("Built by Iqra Ansari")
    st.caption("Tech: Python · SQLite · Gemini API · Streamlit")

# ---------- Header ----------
st.title("🩺 Triage Chatbot")
st.write("Describe your symptoms in plain English, and get possible conditions with urgency levels.")
st.info("⚠️ Educational tool only — not a substitute for professional medical advice.", icon="⚠️")

# ---------- Example prompts ----------
st.write("**Try an example:**")
example_cols = st.columns(3)
examples = [
    "I have a fever, cough, and feel really tired",
    "Sudden chest pain and shortness of breath",
    "Nausea, vomiting, and stomach pain since last night"
]

if "user_text" not in st.session_state:
    st.session_state.user_text = ""

for col, example in zip(example_cols, examples):
    if col.button(example, use_container_width=True):
        st.session_state.user_text = example

# ---------- Input ----------
user_text = st.text_area(
    "Describe how you're feeling:",
    value=st.session_state.user_text,
    placeholder="e.g. I've had a fever and a bad cough for two days, feeling really tired...",
    key="input_box",
    height=100
)

# ---------- Urgency styling helper ----------
def urgency_style(urgency):
    urgency = urgency.lower()
    if "seek care now" in urgency:
        return "🔴", "#fdecea", "#b02a1e"
    elif "high" in urgency:
        return "🟠", "#fff4e5", "#b06a00"
    elif "medium" in urgency:
        return "🟡", "#fffbe5", "#8a6d00"
    else:
        return "🟢", "#eafaf0", "#1e7a44"

# ---------- Run pipeline ----------
if st.button("Check Symptoms", type="primary"):
    if not user_text.strip():
        st.warning("Please describe your symptoms first.")
    else:
        with st.spinner("Reading your symptoms..."):
            symptoms = extract_symptoms(user_text)

        if not symptoms:
            st.error("No recognizable symptoms found. Try describing them differently.")
        else:
            st.success(f"Detected symptoms: {', '.join(symptoms)}")

            results = match_conditions(symptoms)

            if not results:
                st.error("No matching conditions found.")
            else:
                st.subheader("Possible Conditions")

                for condition_name, urgency, score in results[:3]:
                    icon, bg, fg = urgency_style(urgency)
                    st.markdown(
                        f"""
                        <div style="
                            background-color:{bg};
                            border-left: 5px solid {fg};
                            padding: 12px 16px;
                            border-radius: 6px;
                            margin-bottom: 10px;
                        ">
                            <span style="font-size:16px; font-weight:600; color:{fg};">
                                {icon} {condition_name}
                            </span><br>
                            <span style="color:{fg};">Urgency: {urgency} &nbsp;|&nbsp; Match score: {score:.2f}</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with st.spinner("Generating explanation..."):
                    explanation = generate_explanation(symptoms, results)

                st.subheader("Explanation")
                st.write(explanation)
                st.caption("This is an educational tool, not a medical diagnosis.")