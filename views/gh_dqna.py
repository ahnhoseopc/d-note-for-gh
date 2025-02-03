import utils.auth as auth
import utils.genai as genai
import utils.qna as qna

import streamlit as st

# Initialize messages
def initialize_messages():
    # Initialize chat history
    st.session_state.messages = []
    st.session_state.summary_index = 0
    st.session_state.chat_id = ""
    st.session_state.chat_name = "New Chat"

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

@auth.login_required
def main():
    # Initialize user id
    # if "user_id" not in st.session_state:
    #     st.session_state.user_id = "munhwa_user"

    # Initialize messages
    if "messages" not in st.session_state:
        initialize_messages()

    with st.sidebar.container(height=200):
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
                    msgs, name = qna.get_chat_messages(selected_chat["user_id"], selected_chat["chat_id"])
                    st.session_state.messages = msgs
                    st.session_state.chat_name = name
                    st.session_state.chat_id = selected_chat["chat_id"]
                    st.session_state.summary_index = min(0, len(st.session_state.messages) - 1)

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
    #
    # Page title for D-QnA
    #
    st.title("Doctor's QnA")

    # 저장된 챗 메시지 출력 
    st.text(st.session_state.chat_name, help="대화의 제목")
    # Display chat messages from history on app rerun
    for i, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"], avatar="👩‍⚕️" if message["role"] == "user" else "💻"):
            st.markdown(str(i) + ": " + message["parts"][0]["text"])

    #
    # 사용자 Prompt 입력
    #
    SUMMARY_CHAT_COUNT  =10
    if st.chat_input("Medical assistance?", key="prompt"):
        #
        # SUMMARY_CHAT_COUNT 이상 지나면 그동안 질의응답을 요약하여 context를 절약한다.
        #
        if len(st.session_state.messages) - st.session_state.summary_index > SUMMARY_CHAT_COUNT:
            summary_text = qna.summarize_content(st.session_state.messages[st.session_state.summary_index:])
            if summary_text:
                st.session_state.messages.append({"role": "assistant", "parts": [{"text": "<Chat Summary>\n" + summary_text}]})
                st.session_state.summary_index = len(st.session_state.messages) - 1

                with st.chat_message(st.session_state.messages[-1]["role"], avatar="👩‍⚕️" if st.session_state.messages[-1]["role"] == "user" else "💻"):
                    st.markdown(str(len(st.session_state.messages)) + ": " + st.session_state.messages[-1]["parts"][0]["text"])

        # Prompt로 질의용 Content를 만든다.
        doctor_message = {"role": "user", "parts": [{"text": st.session_state.prompt}]}

        # 사용자 Prompt 출력
        with st.chat_message("user", avatar="👩‍⚕️",):
            st.markdown(str(len(st.session_state.messages)) + ": " + st.session_state.prompt)

        # 사용자 Content 저장
        st.session_state.messages.append(doctor_message)

        #
        # LLM에 의한 응답 Content 생성
        #
        llm_responses = qna.generate_content(doctor_message, st.session_state.messages[st.session_state.summary_index:])

        # LLM 응답을 Stream 형식으로 출력 
        with st.chat_message("assistant", avatar="💻"):
            st.markdown(str(len(st.session_state.messages)) + ": ")
            response_text = st.write_stream(llm_responses)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "parts": [{"text": response_text}]})
    # END OF CHAT INPUT

import forms.sidebar as sidebar

if __name__ == "__page__":
    main()
    sidebar.display()
