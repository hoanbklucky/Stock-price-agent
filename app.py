import streamlit as st

#from google.cloud.aiplatform import agent_engines
from vertexai import agent_engines

if "agent" not in st.session_state:
    st.session_state["agent"] = agent_engines.get("projects/533873564462/locations/us-central1/reasoningEngines/8665884457200254976")

if "remote_session" not in st.session_state:
    st.session_state["remote_session"] = st.session_state["agent"].create_session(user_id="hoan_456")

def generate(prompt):
    for event in st.session_state["agent"].stream_query(
        user_id="hoan_456",
        session_id=st.session_state["remote_session"]["id"],
        message=prompt,
    ):
        yield event
        """ if "content" in event:
            if "parts" in event["content"]:
                parts = event["content"]["parts"]
                for part in parts:
                    #if "text" in part:
                    #    text_part = part["text"]
                    yield part """

st.title(" 🤖 CareGuideAI")
st.header("I am a virtual nurse", divider="gray")
st.write("""To be able to assist you, I will ask you some questions related to the patient and then let you know triage decision. I can also provide you general guidance on post tonsillectomy care. Are you ready?""")

if "model" not in st.session_state:
    st.session_state["model"] = "gemini-2.5-pro"

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
    
