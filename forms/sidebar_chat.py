import utils.chat as chat

import logging

import streamlit as st

# SIDEBAR for CHAT HISTORY

# Initialize messages
def initialize_messages(user_id, chat_group):
    logging.debug("enetered")
    # Initialize chat history
    dchat = {
         "user_id": user_id
        ,"chat_group": chat_group # current chat group
        ,"chat_id": "" # current chat
        ,"chat_name": "New Chat" # current chat
        ,"messages": [] # current chat
        ,"chat_list": chat.get_chat_list(user_id, chat_group) # saved chat list 
    }
    return dchat

def load_chat_messages(user_id, chat_group, selected_chat_id):
    logging.debug("enetered")
    msgs, name = chat.get_chat_messages(user_id, chat_group, selected_chat_id)
    dchat = {}
    dchat["user_id"] = user_id
    dchat["chat_group"] = chat_group
    dchat["chat_id"] = selected_chat_id
    dchat["chat_list"] = chat.get_chat_list(user_id, chat_group)
    dchat["chat_name"] = name
    dchat["messages"] = msgs
    logging.debug(f"messages loaded {len(msgs)} messages")
    return dchat

def delete_chat_history(dchat):
    logging.debug("enetered")
    chat.delete_history(dchat["user_id"], dchat["chat_group"], dchat["chat_id"])
    dchat["chat_list"] = chat.get_chat_list(dchat["user_id"], dchat["chat_group"]) # to refresh chat list

def save_chat_history(dchat):
    logging.debug("enetered")
    if dchat["chat_id"] == "":
        dchat["chat_id"] = chat.generate_chat_id(dchat["user_id"])
        dchat["chat_name"] = chat.summarize_title(dchat["messages"])
        logging.debug(f"{dchat["chat_id"]}: {dchat["chat_name"]}")

    chat.save_history(dchat["user_id"], dchat["chat_group"], dchat["chat_id"], dchat["chat_name"], dchat["messages"])
    dchat["chat_list"] = chat.get_chat_list(dchat["user_id"], dchat["chat_group"]) # to refresh chat list
    logging.debug(f"chat_list saved")

def display():
    logging.debug("enetered")
    # Initialize messages
    if "dchat" not in st.session_state:
        st.session_state.dchat = initialize_messages(st.session_state.user_id, "CHAT")
    dchat = st.session_state.dchat

    with st.sidebar.container(height=200):
        # Chat History Management
        st.caption("Chat Management")
        cols = st.columns([1,1])
        with cols[0]:
            if st.button("Delete", use_container_width=True):
                delete_chat_history(dchat)
        with cols[1]:
            if st.button("Save", use_container_width=True):
                if len(dchat["messages"]):
                    save_chat_history(dchat)

        new_chat = {"user_id":dchat["user_id"], "chat_id": "", "chat_name":"New chat"}

        selected_chat = st.selectbox("Chat History", [new_chat] + dchat["chat_list"], key="chat_history", format_func=lambda x: x["chat_name"])
        if selected_chat is not None:
            if selected_chat["chat_id"] != dchat["chat_id"]:
                if selected_chat["chat_name"] == "New chat":
                    dchat = initialize_messages(dchat["user_id"], dchat["chat_group"])
                else:
                    dchat = load_chat_messages(dchat["user_id"], dchat["chat_group"], selected_chat["chat_id"])

                st.session_state.dchat = dchat
            pass
        pass
    pass
