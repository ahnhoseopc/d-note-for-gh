import utils.genai as genai

import numpy as np
import random
import time
import streamlit as st

# Streamed response emulator
def generate_content(prompt, previous_messages=[]):
    model = "medlm"
    responses = genai.generate([prompt] + previous_messages, model)

    return responses

st.title("Medical Assistant: Doctor's QnA")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Medical situation?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "doctor", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("doctor"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        responses = generate_content(prompt, st.session_state.messages)
        response_text = ""
        for response in responses:
            response_text += response.text
            st.markdown(response_text)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
