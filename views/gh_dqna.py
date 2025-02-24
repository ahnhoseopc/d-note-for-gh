import utils.auth as auth
import utils.qna as qna
import forms.sidebar_qna as sidebar_qna
import views.gh_dqna_00 as intro

import streamlit as st

@auth.login_required
def main():
    # Initialize user id
    # if "user_id" not in st.session_state:
    #     st.session_state.user_id = "munhwa_user"

    # Side bar for chat history
    sidebar_qna.display()

    #
    # Page title for D-QnA
    #
    st.title("D-QnA, 전문 의료지식 정보화 Agent")

    tab0, tab1, tab2, tab4 = st.tabs(["의료지식 정보화 Agent", "**Doctor's**", "Expert's", "Researcher's"])

    with tab0:
        intro.intro_record_source()

    with tab1:
        chat_container = st.container()

        with chat_container:
            # 저장된 챗 메시지 출력 
            st.text(st.session_state.chat_name, help="대화의 제목")
            # Display chat messages from history on app rerun
            for i, message in enumerate(st.session_state.messages):
                with st.chat_message(message["role"], avatar="👩‍⚕️" if message["role"] == "user" else "💻"):
                    st.write(str(i) + ": " + message["parts"][0]["text"])

    #
    # 사용자 Prompt 입력
    #
    SUMMARY_CHAT_COUNT  =10
    if st.chat_input("Medical assistance?", key="prompt"):
        with chat_container:
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
