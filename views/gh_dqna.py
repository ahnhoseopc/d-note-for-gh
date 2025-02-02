import utils.genai as genai
import utils.qna as qna

import streamlit as st

# Initialize messages
def initialize_messages():
    # Initialize user id
    if "user_id" not in st.session_state:
        st.session_state.user_id = "munhwa_user"

    # Initialize chat history
    st.session_state.messages = []
    st.session_state.summary_index = 0
    st.session_state.chat_id = qna.generate_chat_id(st.session_state.user_id)
    st.session_state.chat_name = "새 대화"

if "messages" not in st.session_state:
    initialize_messages()

st.title("Doctor's QnA")

def display_chat():
    st.text(st.session_state.chat_name, help="대화의 제목")
    # Display chat messages from history on app rerun
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"], avatar="👩‍⚕️" if message["role"] == "user" else "💻"):
            st.markdown(str(i) + ": " + message["parts"][0]["text"])

# 
display_chat()

def on_submit_chat_input():

    # Generate assistant response
    if len(st.session_state.messages) - st.session_state.summary_index > 10:
        summary_text = qna.summarize_content(st.session_state.messages[st.session_state.summary_index:])
        if summary_text:
            st.session_state.messages.append({"role": "assistant", "parts": [{"text": "<Chat Summary>\n" + summary_text}]})
            st.session_state.summary_index = len(st.session_state.messages) - 1

            with st.chat_message(st.session_state.messages[-1]["role"], avatar="👩‍⚕️" if st.session_state.messages[-1]["role"] == "user" else "💻"):
                st.markdown(str(len(st.session_state.messages)) + ": " + st.session_state.messages[-1]["parts"][0]["text"])

    doctor_message = {"role": "user", "parts": [{"text": st.session_state.prompt}]}

    # Display user message in chat message container
    with st.chat_message("user", avatar="👩‍⚕️",):
        st.markdown(str(len(st.session_state.messages)) + ": " + st.session_state.prompt)

    # Add user message to chat history
    st.session_state.messages.append(doctor_message)

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="💻"):
        st.markdown(str(len(st.session_state.messages)) + ": ")
        response_text = st.write_stream(qna.generate_content(doctor_message, st.session_state.messages[st.session_state.summary_index:]))

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "parts": [{"text": response_text}]})
    pass

if st.chat_input("Medical assistance?", key="prompt"):
    on_submit_chat_input()

with st.sidebar.container(height=300):
    cols = st.columns([1,1])
    with cols[0]:
        if st.button("New Chat", use_container_width=True):
            if len(st.session_state.messages):
                qna.save_history(st.session_state.user_id, st.session_state.chat_id, st.session_state.messages)
            initialize_messages()
            st.session_state.chat_history = None
    with cols[1]:
        if st.button("Save Chat", use_container_width=True):
            if len(st.session_state.messages):
                qna.save_history(st.session_state.user_id, st.session_state.chat_id, st.session_state.messages)

    links = [
        {"name": "Early Gastric Cancer Diagnosis", "user_id":"munhwa_user", "chat_id": "20250202_153648_fkxv"},
        {"name": "Gastric Cancer Surgery Report", "user_id":"munhwa_user", "chat_id": "20250202_020514_nguv"},
        {"name": "Lung Cancer Epidemiology", "user_id":"munhwa_user", "chat_id": "20250202_015321_chpc"}
    ]

    # for link in links:
    #     if st.button(link["name"], key=link["chat_id"]):
    #         msgs, name = qna.get_history(link["user_id"], link["chat_id"])
    #         st.session_state.messages = msgs
    #         st.session_state.chat_name = name
    if selected := st.selectbox("기존 대화", links, key="chat_history", index=None, format_func=lambda x: x["name"]):
        link = selected
        msgs, name = qna.get_history(link["user_id"], link["chat_id"])
        st.session_state.messages = msgs
        st.session_state.chat_name = name

    # for link in links:
    #     if st.button(link["name"]):
    #         webbrowser.open(link["url"])
