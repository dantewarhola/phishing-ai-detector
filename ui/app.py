import streamlit as st
import requests

# Streamlit UI for Phish-AI Detector
st.set_page_config(page_title="Phish‑AI Detector", layout="centered")
st.title("🛡️ Phish‑AI Email Detector - Made by: Dante Warhola")

st.markdown(
    "Paste your email below. 0–50% ⇒ **⚠️ Phishing**, 51–75% ⇒ **🤔 Unsure**, 76–100% ⇒ **✅ Safe**."
)

email_text = st.text_area("Email Text", height=300)

if st.button("Check Email"):
    if not email_text.strip():
        st.warning("Please enter some email text above.")
    else:
        with st.spinner("Analyzing…"):
            try:
                resp = requests.post(
                    "http://localhost:8000/predict",
                    json={"text": email_text}
                )
                data = resp.json()
                score = data.get("score", 0.0)
                pct   = score * 100

                # Bucket the score
                if pct <= 50:
                    st.error(f"⚠️ Phishing (score: {pct:.1f}%)")
                elif pct <= 75:
                    st.warning(f"🤔 Unsure (score: {pct:.1f}%)")
                else:
                    st.success(f"✅ Safe (score: {pct:.1f}%)")

            except requests.exceptions.RequestException as e:
                st.error(f"Error communicating with API: {e}")
