import streamlit as st
import csv
import io
import json
import os

from google.cloud.aiplatform import agent_engines

agent = agent_engines.get("8914989811589185536")

remote_session = agent.create_session(user_id="u_456")

def generate(prompt):
    for event in agent.stream_query(
        user_id="u_456",
        session_id=remote_session["id"],
        message=prompt,
    ):
        if "text" in event["content"]["parts"][0]:
            yield event["content"]["parts"][0]["text"]

st.title(" 🤖 Virtual Nurse")
st.header("I am a virtual nurse", divider="gray")
st.write("""To be able to assist you, I will ask you some questions related to the patient and then let you know triage decision. I can also provide you general guidance on post tonsillectomy care. Are you ready?""")

if "model" not in st.session_state:
    st.session_state["model"] = "gemini-2.5-flash-001"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "contents" not in st.session_state:
    st.session_state.contents = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.contents.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("model"):
        response = st.write_stream(generate(prompt))

    st.session_state.messages.append({"role": "model", "content": response})
    st.session_state.contents.append({"role": "model", "content": response})
    print(st.session_state.contents)
    
