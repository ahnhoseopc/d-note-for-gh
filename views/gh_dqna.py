import logging
import utils.auth as auth
import utils.qna as qna

import forms.sidebar_qna as sidebar_qna
import views.gh_dqna_00 as intro

import streamlit as st

# Initialize messages
def initialize_messages(chat_group):
    # Initialize chat history
    st.session_state[chat_group] = {
         "user_id": st.session_state.user_id
        ,"chat_group": chat_group # current chat group
        ,"chat_id": "" # current chat
        ,"chat_name": "New Chat" # current chat
        ,"chat_msgs": [] # current chat
        ,"chat_list": qna.get_chat_list(st.session_state.user_id) # saved chat list 
    }

def show_chat_input(chat_input):
    # 사용자 Prompt 출력
    with st.chat_message("user", avatar="👩‍⚕️",):
        st.markdown(chat_input["parts"][0]["text"])

def show_chat_response(chat_response):
    # 시스템 Response 출력
    with st.chat_message("assistant", avatar="💻"):
        st.markdown(chat_response["parts"][0]["text"])

def stream_chat_response(llm_responses):
    # 시스템 Response 출력
    response_text = ""
    with st.chat_message("assistant", avatar="💻"):
        response_text = st.write_stream(llm_responses)
    return response_text

def summarize_recent_qna(messages, display_chat=True):
    summary_request = {"role": "user", "parts": [{"text": "<Chat Summary>"}]}
    if display_chat:
        show_chat_input(summary_request)

    summary_text = qna.summarize_content(messages)

    summary_message = {"role": "assistant", "parts": [{"text": summary_text}]}
    if display_chat:
        show_chat_response(summary_message)

    return summary_request, summary_message

@auth.login_required
def main():
    # Side bar for chat history
    sidebar_qna.display()

    #
    # Page title for D-QnA
    #
    st.title("D-QnA, 전문 의료지식 정보화 Agent")

    tab0, tab1, tab2, tab3 = st.tabs(["의료지식 정보화 Agent", "**Doctor's**", "Expert's", "Researcher's"])

    with tab0:
        intro.intro_record_source()

    with tab2:
        st.write("서비스 준비중입니다.")
    with tab3:
        st.write("서비스 준비중입니다.")

    with tab1:
        cols = st.columns([8,2], vertical_alignment='bottom')
        with cols[0]:
            chat_container = st.container()
            with chat_container:
                # 저장된 챗 메시지 출력 
                st.text(st.session_state.chat_name, help="대화의 제목")
                # Display chat messages from history on app rerun
                for i, message in enumerate(st.session_state.messages):
                    if message["role"] == "user":
                        show_chat_input(message)
                    if message["role"] == "assistant":
                        show_chat_response(message)
        with cols[1]:
            sub_container = st.container()
            with sub_container:
                if st.button("##### 대화 요약  "):
                    _,summary = summarize_recent_qna(st.session_state.messages[st.session_state.summary_index:], False)
                    st.markdown(summary["parts"][0]["text"])
                # else:
                #     for i, message in enumerate(st.session_state.messages, start=0):
                #         if message["role"] == "user" and message["parts"][0]["text"] == "<Chat Summary>":
                #             st.markdown(st.session_state.messages[i+1]["parts"][0]["text"])
                #             break

    #
    # 사용자 Prompt 입력
    #
    SUMMARY_CHAT_COUNT  = 10
    if st.chat_input("Medical assistance?", key="prompt"):
        with chat_container:
            #
            # SUMMARY_CHAT_COUNT 이상 지나면 그동안 질의응답을 요약하여 context를 절약한다.
            #
            if len(st.session_state.messages) - st.session_state.summary_index > SUMMARY_CHAT_COUNT:
                summary_request, summary_message = summarize_recent_qna(st.session_state.messages[st.session_state.summary_index:])

                st.session_state.messages.append(summary_request)
                st.session_state.messages.append(summary_message)

                st.session_state.summary_index = len(st.session_state.messages) - 1

                with sub_container:
                    st.markdown("##### 대화 요약  ")
                    st.markdown(summary_message["parts"][0]["text"])



            # Prompt로 질의용 Content를 만든다.
            doctor_message = {"role": "user", "parts": [{"text": st.session_state.prompt}]}
            show_chat_input(doctor_message)

            st.session_state.messages.append(doctor_message)

            #
            # LLM에 의한 응답 Content 생성
            #
            llm_responses = qna.generate_content(doctor_message, st.session_state.messages[st.session_state.summary_index:])
            response_text = stream_chat_response(llm_responses)

            assistant_message = {"role": "assistant", "parts": [{"text": response_text}]}
            st.session_state.messages.append(assistant_message)
    # END OF CHAT INPUT

import forms.sidebar as sidebar

if __name__ == "__page__":
    main()
    sidebar.display()
