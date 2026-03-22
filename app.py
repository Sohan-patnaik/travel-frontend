import os
import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "https://travel-backend-production-a2c6.up.railway.app")
REQUEST_TIMEOUT = 120 

st.set_page_config(
    page_title="AI Travel Agent",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stChatMessage { border-radius: 12px; }
    .st-emotion-cache-1c7y2kd { background: #f0f4ff; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("✈️ AI Travel Agent")
st.caption("Plan trips · check flights, trains & hotels · get weather updates")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask anything about your trip…")

if query:
    query = query.strip()
    if not query:
        st.warning("Please enter a valid question.")
        st.stop()

    if len(query) > 1000:
        st.warning("Query is too long. Please keep it under 1000 characters.")
        st.stop()


    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)


    with st.chat_message("assistant"):
        with st.spinner("Planning your trip… ✈️"):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/agent",
                    json={"query": query},
                    timeout=REQUEST_TIMEOUT,
                )

                if response.status_code == 200:
                    data = response.json()
                    reply = data.get("reply", "No response received.")
                    duration = data.get("duration_ms")
                    if duration:
                        reply += f"\n\n*⏱ Answered in {duration / 1000:.1f}s*"

                elif response.status_code == 422:
                    reply = "⚠️ Invalid input. Please rephrase your question."

                elif response.status_code == 500:
                    reply = "⚠️ The server encountered an error. Please try again shortly."

                else:
                    reply = f"⚠️ Unexpected error (HTTP {response.status_code}). Please try again."

            except requests.Timeout:
                reply = "⏳ The request timed out. The agent is taking too long — please try again."
            except requests.ConnectionError:
                reply = "🔌 Cannot reach the server. Please check your connection or try again later."
            except Exception as e:
                reply = f"⚠️ Unexpected error: {str(e)}"

        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})