import utils.qna as qna

import streamlit as st


# Initialize messages
def initialize_messages():
    # Initialize chat history
    st.session_state.messages = []
    st.session_state.summary_index = 0
    st.session_state.chat_id = qna.generate_chat_id(st.session_state.user_id)
    st.session_state.chat_name = "New Chat"
    pass

def load_chat_history(selected_chat):
    msgs, name = qna.get_chat_messages(selected_chat["prefix"], selected_chat["chat_id"])
    st.session_state.messages = msgs
    st.session_state.chat_name = name
    st.session_state.chat_id = selected_chat["chat_id"]
    st.session_state.summary_index = min(0, len(st.session_state.messages) - 1)
    pass

# SIDEBAR for CHAT HISTORY
def delete_chat_history():
    if st.session_state.chat_id == "":
        initialize_messages()
    else:
        qna.delete_history(st.session_state.user_id, st.session_state.chat_id)
        st.session_state.chat_list = None       # to refresh chat list
    pass

def save_chat_history():
    if st.session_state.chat_id == "":
        st.session_state.chat_id = qna.generate_chat_id(st.session_state.user_id)
        st.session_state.chat_name = qna.summarize_title(st.session_state.messages)
        st.session_state.chat_list = None       # to refresh chat list

    qna.save_history(st.session_state.user_id, st.session_state.chat_id, st.session_state.chat_name, st.session_state.messages)

def display():
    # Initialize messages
    if "messages" not in st.session_state:
        initialize_messages()

    with st.sidebar.container(height=200):
        # Chat History Management
        st.caption("Chat Management")
        cols = st.columns([1,1])
        # with cols[0]:
            # if st.button("New Chat", use_container_width=True):
            #     if len(st.session_state.messages):
            #         save_chat_history()
            #     initialize_messages()
                # st.session_state.chat_history = None   # to unselect old chat for the new chat
        with cols[0]:
            if st.button("Delete", use_container_width=True):
                delete_chat_history()
        with cols[1]:
            if st.button("Save", use_container_width=True):
                if len(st.session_state.messages):
                    save_chat_history()

        # Chat History Selector
        selected_index = 0
        if "chat_list" not in st.session_state or st.session_state.chat_list is None:
            st.session_state.chat_list = qna.get_chat_list(st.session_state.user_id)
            indices = [i for i, item in enumerate(st.session_state.chat_list) if item['chat_id'] == st.session_state.chat_id]
            if len(indices):
                selected_index = indices[0]

        new_chat = {"chat_name":"New chat", "user_id":st.session_state.user_id, "chat_id": ""}

        selected_chat = st.selectbox("Chat History", [new_chat]+st.session_state.chat_list, key="chat_history", index=selected_index, format_func=lambda x: x["chat_name"])
        if selected_chat is not None:
            if selected_chat["chat_id"] != st.session_state.chat_id:
                if selected_chat["chat_name"] == "New chat":
                    initialize_messages()
                else:
                    load_chat_history(selected_chat)
