import streamlit as st
from groq import Groq

# Load API key from secrets
API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=API_KEY)

st.set_page_config(page_title="Groq Chat", page_icon="🤖")
st.title("🤖 Groq Chat App")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_container = st.empty()
        reply = ""

        stream = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=st.session_state.messages,
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content:
                reply += chunk.choices[0].delta.content
                response_container.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
