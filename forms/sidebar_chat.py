import utils.chat as chat

import streamlit as st

# SIDEBAR for CHAT HISTORY
def delete_chat_history(dchat):
    chat.delete_history(dchat["user_id"], dchat["chat_id"])
    dchat["chat_list"] = chat.get_chat_list(dchat["user_id"]) # to refresh chat list

def save_chat_history(dchat):
    if dchat["chat_id"] == "":
        dchat["chat_id"] = chat.generate_chat_id(dchat["user_id"])
        dchat["chat_name"] = chat.summarize_title(dchat["chat_msgs"])

    chat.save_history(dchat["user_id"], dchat["chat_id"], dchat["chat_name"], dchat["chat_msgs"])
    dchat["chat_list"] = chat.get_chat_list(dchat["user_id"]) # to refresh chat list

def load_chat_history(dchat, selected_chat):
    if selected_chat["chat_id"] != "":
        msgs, name = chat.get_chat_messages(selected_chat["prefix"], selected_chat["chat_id"])
        dchat["chat_id"] = selected_chat["chat_id"]
        dchat["chat_name"] = name
        dchat["chat_msgs"] = msgs

def display(dchat):
    with st.sidebar.container(height=200):
        # Chat History Management
        st.caption("Chat Management")
        cols = st.columns([1,1])
        with cols[0]:
            if st.button("Delete", use_container_width=True):
                delete_chat_history()
        with cols[1]:
            if st.button("Save", use_container_width=True):
                if len(dchat["chat_msgs"]):
                    save_chat_history(dchat)

        # Chat History Selector
        selected_index = 0
        indices = [i for i, item in enumerate(dchat["chat_list"]) if item['chat_id'] == dchat["chat_id"]]
        if len(indices):
            selected_index = indices[0]

        new_chat = {"user_id":dchat["user_id"], "chat_id": "", "chat_name":"New chat"}

        selected_chat = st.selectbox("Chat History", [new_chat] + dchat["chat_list"], key="chat_history", index=selected_index, format_func=lambda x: x["chat_name"])
        if selected_chat is not None:
            if selected_chat["chat_id"] != dchat["chat_id"]:
                if selected_chat["chat_name"] != "New chat":
                    load_chat_history(selected_chat)