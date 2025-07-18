# app_ui.py

import streamlit as st
from agent import create_triage_agent

# Create the AI agent once
triage_agent = create_triage_agent()

# Streamlit UI setup
st.set_page_config(page_title="VulnSage", layout="centered")
st.title("🔎 VulnSage - AI Vulnerability Triage")

# Input area
report_text = st.text_area("📝 Paste your vulnerability report below:", height=250)

# Button to trigger analysis
if st.button("Triage Vulnerability"):
    if report_text.strip():
        with st.spinner("Analyzing..."):
            try:
                result = triage_agent.invoke({"report_text": report_text})
                cleaned = str(result.content)  # Safely extract the content

                st.markdown(f"### 🧠 Triage Result\n{cleaned}", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a report to triage.")
