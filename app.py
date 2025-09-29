import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Wellness Assistant Chatbot", page_icon="💬")
st.title("💬 Wellness Assistant Chatbot")
st.write("Chat with your personal wellness assistant. Confide, ask for motivation, or simply say hello!")

# Generate a unique user id per session
if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())

backend_url = "http://localhost:8000/chat"

if "messages" not in st.session_state:
    st.session_state["messages"] = []

def send_message(msg):
    payload = {"user_id": st.session_state["user_id"], "message": msg}
    resp = requests.post(backend_url, json=payload)
    return resp.json()["response"]

with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your message:", "")
    submitted = st.form_submit_button("Send")
    if submitted and user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        bot_reply = send_message(user_input)
        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")