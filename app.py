import streamlit as st
import requests

st.set_page_config(page_title="AI Travel Agent", page_icon="✈️", layout="centered")

st.title("✈️ AI Travel Agent")
st.caption("Plan trips, check flights, hotels, trains, and budget")


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


query = st.chat_input("Ask your travel query...")

if query:

    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)


    with st.chat_message("assistant"):
        with st.spinner("Planning your trip... ✈️"):

            try:
                response = requests.post(
                    "https://travel-backend-production-a2c6.up.railway.app/agent",
                    json={"query": query}
                )

                if response.status_code == 200:
                    data = response.json()
                    reply = data.get("reply", "No response from agent")

                else:
                    reply = f"API Error: {response.text}"

            except Exception as e:
                reply = f"Connection Error: {e}"

            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})