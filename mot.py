import streamlit as st
import google.generativeai as genai
import requests

# ------------------------------------------
# ✅ HARDCODED CONFIG SECTION (EDIT THIS)
# ------------------------------------------
GEMINI_API_KEY = "AIzaSyC-XC5GyRY5YPHcqeTEPjGspHSEn1P4cqM"  # Replace with your real key
WEBHOOK_URL = "https://mukilan114.app.n8n.cloud/webhook-test/Responsse"  # Optional: Set your webhook receiver URL

# ------------------------------------------
# ✅ Gemini Configuration
# ------------------------------------------
try:
    genai.configure(api_key="AIzaSyC-XC5GyRY5YPHcqeTEPjGspHSEn1P4cqM")
except Exception as e:
    st.error(f"❌ Failed to configure Gemini API: {e}")
    st.stop()

# ------------------------------------------
# ✅ Streamlit UI Setup
# ------------------------------------------
st.set_page_config(page_title="🎯 Goal Tracker & Motivation", layout="centered")
st.title("🎯 AI Goal Tracker with Motivational Quotes")

# User Inputs
st.subheader("📝 Define Your Goal")
goal_category = st.selectbox("Select a Goal Category", [
    "Fitness", "Career", "Education", "Mental Health", "Finance", "Personal Growth", "Other"
])
goal_description = st.text_input("Describe your specific goal:")

# Generate motivation using Gemini
if st.button("✨ Get Tip & Motivation"):
    if not goal_description.strip():
        st.warning("Please enter your goal description.")
    else:
        with st.spinner("Talking to Gemini Flash... 🤖"):
            try:
                prompt = f"""
You are a motivational AI helping users accomplish goals.

Goal Category: {goal_category}
Goal Description: {goal_description}

Respond with:
1. A short practical tip for the day.
2. A unique motivational quote using emojis.

Limit response to under 100 words.
"""

                # Use gemini-1.5-flash
                chat = genai.GenerativeModel("gemini-1.5-flash").start_chat()
                result = chat.send_message(prompt)

                st.success("✅ Here's your AI-powered tip:")
                st.markdown(result.text)

                # Optionally send to webhook
                if WEBHOOK_URL:
                    try:
                        payload = {
                            "category": goal_category,
                            "description": goal_description,
                            "response": result.text
                        }
                        res = requests.post(WEBHOOK_URL, json=payload)
                        if res.status_code == 200:
                            st.info("📡 Sent result to webhook successfully.")
                        else:
                            st.warning(f"Webhook returned status {res.status_code}")
                    except Exception as e:
                        st.warning(f"Could not send to webhook: {e}")

            except Exception as e:
                st.error(f"Failed to get response from Gemini: {e}")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Gemini Flash · Python 3.13.4 · No external env")
