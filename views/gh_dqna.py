import utils.genai as genai

import numpy as np
import random
import time
import streamlit as st

response_text = ""

# Streamed response emulator
def generate_content(message, previous_messages=[]):
    global response_text

    model = "medlm"
    # responses = genai.generate( ["이전 메시지를 요약하시오."] +  previous_messages, model)
    # summary = {"role": "system", "parts": [responses[0].text]}

    responses = genai.generate( previous_messages + [message] , model)

    response_text = ""
    for response in responses:
        response_text += response.text
        yield response.text
    
st.title("Medical Assistant: Doctor's QnA")

if st.button("Reset chat history"):
    st.session_state.messages = []

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"][0]["text"])

# Accept user input
if prompt := st.chat_input("Medical situation?"):
    doctor_message = {"role": "user", "parts": [{"text": prompt}]}

    # Display user message in chat message container
    with st.chat_message("doctor"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.write_stream(generate_content(doctor_message, st.session_state.messages))

    # Add user message to chat history
    st.session_state.messages.append(doctor_message)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "parts": [{"text": response_text}]})
