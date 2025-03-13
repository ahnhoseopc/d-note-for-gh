import time

import urllib
import utils.auth as auth
import utils.base as base
import utils.chat as chat
import forms.sidebar_qna as sidebar_qna
import views.gh_dchat_00 as intro

import streamlit as st

def show_references_filter(references, filter_text, filter_answer):
    cols = st.columns(5)
    with cols[0]:
        if references:
            with st.popover("References"):
                for ref in references:
                    st.markdown(f"* [{base.make_short(ref['title'], 60)}]({urllib.parse.quote(ref['url_page'], safe=":/?#=", encoding="utf-8")})")
                    st.markdown(f"  `page: {ref['pageIdentifier']}` `relevance: {ref['relevanceScore']}`")
                    st.markdown(f"  `{ref['content']}`")
    with cols[1]:
        if filter_text:
            with st.popover("Filtered Text"):
                st.markdown(f"{filter_text}")
                st.write("##### Filter answer:")
                st.json(filter_answer)

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
                        show_references_filter(message["references"] if "references" in message else []
                                        , message["filter_text"] if "filter_text" in message else None
                                        , message["filter_answer"] if "filter_answer" in message else None)

        with col2:
            sub_container = st.container()
            with sub_container:
                st.markdown("##### 관련 규정")
                st.markdown("* 요양급여의 적용기준 및 방법에 관한 세부사항")

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
                st.session_state.related_qna_list = chat_response["related_qna_list"]

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant"
                                                  , "parts": [{"text": chat_response["answer_text"]}]
                                                  , "references": chat_response["references"]
                                                  , "filter_text": chat_response["filter_text"] if "filter_text" in chat_response else None
                                                  , "filter_answer": chat_response["filter_answer"] if "filter_answer" in chat_response else None})

                # LLM 응답을 Stream 형식으로 출력 
                with st.chat_message("assistant", avatar="💻"):
                    if "answer_text" in chat_response:
                        st.markdown(f"{len(st.session_state.messages)}: {chat_response["answer_text"]}")
                    if "references" in chat_response:
                        show_references_filter(chat_response["references"]
                                                , chat_response["filter_text"] if "filter_text" in chat_response else None
                                                , chat_response["filter_answer"] if "filter_answer" in chat_response else None)

    if "chat_response" in st.session_state:
        if "related_qna_list" in st.session_state.chat_response:
                qna_num = len(st.session_state["chat_response"]["related_qna_list"])
                cols = st.columns(qna_num)
                for i, qna in enumerate(st.session_state["chat_response"]["related_qna_list"]):
                    with cols[i]:
                        interested = st.button(f"{i+1}. {base.make_short(qna["question"])}", help=qna["question"], use_container_width=True)
                        st.link_button(f"[{base.make_short(qna['document_title'])}]", qna["document_uri"], help=qna["document_title"], use_container_width=True)
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
