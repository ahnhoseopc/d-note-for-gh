import time
import utils.auth as auth
import utils.base as base
import utils.chat as chat
import forms.sidebar_qna as sidebar_qna
import views.gh_dchat_00 as intro

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
    st.title("D-Chat, 전문 의료업무 정보 Agent")

    tab0, tab1, tab2 = st.tabs(["의료업무 정보화 Agent", "**요양급여규정 안내**", "보험심사청구 업무"])

    with tab0:
        intro.intro_record_source()

    with tab1:
        col1, col2 = st.columns([8,2])
        with col1:
            chat_container = st.container()
            with chat_container:
            
                # 저장된 챗 메시지 출력 
                st.text(st.session_state.chat_name, help="채팅 제목")
                # Display chat messages from history on app rerun
                for i, message in enumerate(st.session_state.messages):
                    with st.chat_message(message["role"], avatar="👩‍⚕️" if message["role"] == "user" else "💻"):
                        st.markdown(str(i) + ": " + message["parts"][0]["text"])
        with col2:
            st.markdown(
                """
                <style>
                    .bottom-container {
                        display: flex;
                        flex-direction: column;
                        justify-content: flex-end;
                        height: 300px; /* 원하는 높이 설정 */
                    }
                </style>
                """,
                unsafe_allow_html=True
            )
            sub_container = st.container()
            with sub_container:
                st.markdown('<div class="bottom-container">', unsafe_allow_html=True)
                st.markdown("##### 관련 규정")
                st.markdown("* 요양급여의 적용기준 및 방법에 관한 세부사항")

                st.markdown("##### Related Q*A")
                if "chat_response" in st.session_state:
                    if "related_qna_list" in st.session_state.chat_response:
                        for i, qna in enumerate(st.session_state["chat_response"]["related_qna_list"]):
                            st.markdown(f"{i+1}. {base.make_short(qna["question"])}")
                            st.markdown(f"* [{base.make_short(qna["document_title"])}]({qna["document_uri"]}) ")
                else:
                    st.markdown("* No related Q&A")
                st.markdown('</div>', unsafe_allow_html=True)
                pass

    #
    # 사용자 Prompt 입력
    #
    SUMMARY_CHAT_COUNT  =10
    if st.chat_input("Medical assistance?", key="prompt"):
        with chat_container:
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
            chat_response = chat.generate_content(doctor_message["parts"][0]["text"])
            if chat_response:
                st.session_state.chat_response = chat_response

                print(chat_response)
                # if "answer_text" in chat_response:
                #     st.write(chat_response["answer_text"])

                # LLM 응답을 Stream 형식으로 출력 
                with st.chat_message("assistant", avatar="💻"):
                    if "answer_text" in chat_response:
                        st.markdown(f"{len(st.session_state.messages)}: {chat_response["answer_text"]}")

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "parts": [{"text": chat_response["answer_text"]}]})

    if "chat_response" in st.session_state:
        if "related_qna_list" in st.session_state.chat_response:
                qna_num = len(st.session_state["chat_response"]["related_qna_list"])
                cols = st.columns(qna_num)
                for i, qna in enumerate(st.session_state["chat_response"]["related_qna_list"]):
                    with cols[i]:
                        interested = st.button(f"{i+1}. {base.make_short(qna["question"])}", use_container_width=True)
                        if interested:
                            # 사용자 Prompt 출력
                            with chat_container.chat_message("user", avatar="👩‍⚕️",):
                                st.markdown(f"{len(st.session_state.messages)}: {qna["question"]}")

                            # 사용자 Content 저장
                            doctor_message = {"role": "user", "parts": [{"text": qna["question"]}]}
                            st.session_state.messages.append(doctor_message)

                            time.sleep(0.4)

                            # 시스템 Content 출력
                            with chat_container.chat_message("assistant", avatar="💻"):
                                st.markdown(f"{len(st.session_state.messages)}: {qna["answer"]}")

                            # 시스템 Content 저장
                            assistant_message = {"role": "assistant", "parts": [{"text": qna["answer"]}]}
                            st.session_state.messages.append(assistant_message)

                    # st.markdown(f"* [{base.make_short(qna["document_title"])}]({qna["document_uri"]}) ")
        # END OF CHAT INPUT

import forms.sidebar as sidebar

if __name__ == "__page__":
    main()
    sidebar.display()
