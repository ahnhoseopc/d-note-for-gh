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
    st.session_state.conversation_id = qna.generate_conversation_id(st.session_state.user_id)

if "messages" not in st.session_state:
    initialize_messages()

st.title("Medical Assistant: Doctor's QnA")

def on_submit_chat_input():

    # Display chat messages from history on app rerun
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"], avatar="👩‍⚕️" if message["role"] == "user" else "💻"):
            st.markdown(str(i) + ": " + message["parts"][0]["text"])

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

cols = st.columns([6,1,1])
with cols[0]:
    # Accept user input
    if st.chat_input("Medical assistance?", key="prompt"):
        on_submit_chat_input()

with cols[1]:
    if st.button("New Chat"):
        qna.save_history(st.session_state.user_id, st.session_state.conversation_id, st.session_state.messages)
        initialize_messages()
with cols[2]:
    if st.button("Save Chat"):
        qna.save_history(st.session_state.user_id, st.session_state.conversation_id, st.session_state.messages)
