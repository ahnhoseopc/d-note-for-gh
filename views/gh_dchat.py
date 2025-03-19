import time
import urllib

import utils.auth as auth
import utils.base as base
import utils.chat as chat

import forms.sidebar_chat as sidebar_chat
import views.gh_dchat_00 as intro

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
        ,"chat_list": chat.get_chat_list(st.session_state.user_id) # saved chat list 
    }

def show_chat_input(chat_input):
    # 사용자 Prompt 출력
    with st.chat_message("user", avatar="👩‍⚕️",):
        st.markdown(chat_input["parts"][0]["text"])

def show_chat_response(chat_response):
    # 시스템 Response 출력
    with st.chat_message("assistant", avatar="💻"):
        if "filter_text" in chat_response and chat_response["filter_text"]:
            st.markdown( f"{1}: {chat_response["filter_text"]}" )
            with st.container(border=True):
                if "filter_answer" in chat_response and chat_response["filter_answer"] and "citedChunks" in chat_response["filter_answer"]:
                    chunks = chat_response["filter_answer"]["citedChunks"]
                else:
                    chunks = []
                for chunk in chunks:
                    st.markdown( f"{chunk['chunkText']} [참조 {chunk['source']}]({urllib.parse.quote(chunk['url_page'], safe=':/?#=', encoding='utf-8')})" )
        else:
            st.markdown( chat_response["parts"][0]["text"] )

        if "references" in chat_response:
            show_references(chat_response["references"]
                            , chat_response["filter_text"] if "filter_text" in chat_response else None
                            , chat_response["filter_answer"] if "filter_answer" in chat_response else None)
        pass

def show_references(references, filter_text, filter_answer):
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

# def show_related_qna(chat_container, dchat, related_qna_list):
#     with chat_container:
#         st.markdown("###### 관련 질문")
#         qna_num = len(related_qna_list)
#         cols = st.columns(qna_num)
#         for i, qna in enumerate(related_qna_list):
#             with cols[i]:
#                 interested = st.button(f"{i+1}. {base.make_short(qna["question"])}", help=qna["question"], use_container_width=True)

#                 if interested:
#                     # 사용자 Prompt 출력
#                     user_message = {"role": "user", "parts": [{"text": qna["question"]}]}
#                     show_chat_input(user_message)

#                     # 잠시 대기
#                     time.sleep(0.4)

#                     # 시스템 Content 출력
#                     reference_text = f" [ [참조]({urllib.parse.quote(qna['document_uri'], safe=':/?=#', encoding='utf-8')}) ]"
#                     assistant_message = {"role": "assistant", "parts": [{"text": qna["answer"] + reference_text}]}
#                     show_chat_response(assistant_message)
#     pass

def show_related_qna(this_container, chat_container, related_qna_list):
    with this_container:
        st.markdown("###### 관련 질문")
        for i, qna in enumerate(related_qna_list):
            interested = st.button(f"{i+1}. {base.make_short(qna["question"])}", help=qna["question"], use_container_width=True)

            if interested:
                with chat_container:
                    # 사용자 Prompt 출력
                    user_message = {"role": "user", "parts": [{"text": qna["question"]}]}
                    show_chat_input(user_message)

                    # 잠시 대기
                    time.sleep(0.4)

                    # 시스템 Content 출력
                    # reference_text = f" [ [참조]({urllib.parse.quote(qna['document_uri'], safe=':/?=#', encoding='utf-8')}) ]"
                    reference_text = f" [ [참조]({qna['document_uri']}) ]"
                    assistant_message = {
                        "role": "assistant", 
                        "parts": [{"text": qna["answer"] + reference_text}],
                        "related_qna_list": related_qna_list
                        }
                    show_chat_response(assistant_message)

                    return user_message, assistant_message
    return None, None

@auth.login_required
def main():
    # Initialize messages
    #
    # For first tab: 
    CHATGROUP01 = "CHAT"
    if CHATGROUP01 not in st.session_state:
        initialize_messages(CHATGROUP01)
    dchat = st.session_state[CHATGROUP01]

    # Side bar for chat history
    sidebar_chat.display(dchat)

    #
    # Page title for D-QnA
    #
    st.title("D-Chat, 전문 의료업무 정보 Agent")

    tab0, tab1, tab2 = st.tabs(["의료업무 정보화 Agent", "**요양급여규정 안내**", "보험심사청구 업무"])

    with tab0:
        intro.intro_record_source()

    with tab1:
        col1, col2 = st.columns([8,2], vertical_alignment='bottom')
        with col1:
            chat_container = st.container()
            with chat_container:
                # 저장된 챗 메시지 출력 
                st.text(dchat["chat_name"], help="채팅 제목")

                # Display chat messages from history on app rerun
                for i, message in enumerate(dchat["chat_msgs"]):
                    if message["role"] == "user":
                        show_chat_input(message)
                    else:
                        show_chat_response(message)
        with col2:
            sub_container = st.container()
            with sub_container:
                st.markdown("###### 관련 규정")
                st.markdown("* 요양급여의 적용기준 및 방법에 관한 세부사항")

                if dchat["chat_msgs"] and "related_qna_list" in dchat["chat_msgs"][-1]:
                    related_qna_list = dchat["chat_msgs"][-1]["related_qna_list"]
                    a,b = show_related_qna(sub_container, chat_container, related_qna_list)
                    if a and b:
                        dchat["chat_msgs"].append(a)
                        dchat["chat_msgs"].append(b)

    #
    # 사용자 Prompt 입력
    #
    SUMMARY_CHAT_COUNT = 10
    if st.chat_input("Any assistance?", key="chat_prompt"):
        chat_prompt = st.session_state.chat_prompt

        with chat_container:
            
            # Prompt로 질의용 Content를 만든다.
            user_message = {"role": "user", "parts": [{"text": chat_prompt}]}

            # 사용자 Content 저장
            dchat["chat_msgs"].append(user_message)

            # 사용자 Prompt 출력
            show_chat_input(user_message)

            #
            # LLM에 의한 응답 Content 생성
            #
            chat_response = chat.generate_content(chat_prompt)
            if chat_response:
                # Add assistant response to chat history
                response_message = {"role": "assistant"
                                    , "parts": [{"text": chat_response["answer_text"]}]
                                    , "related_qna_list": chat_response["related_qna_list"]
                                    , "references": chat_response["references"]
                                    , "filter_text": chat_response["filter_text"] if "filter_text" in chat_response else None
                                    , "filter_answer": chat_response["filter_answer"] if "filter_answer" in chat_response else None
                                    }

                dchat["chat_msgs"].append(response_message)

                # LLM 응답을 Stream 형식으로 출력 
                # with st.chat_message("assistant", avatar="💻"):
                show_chat_response(response_message)
                st.rerun()

    # if dchat["chat_msgs"] and "related_qna_list" in dchat["chat_msgs"][-1]:
    #     related_qna_list = dchat["chat_msgs"][-1]["related_qna_list"]
    #     show_related_qna(sub_container, chat_container, related_qna_list)
    # END OF CHAT INPUT

import forms.sidebar as sidebar

if __name__ == "__page__":
    main()
    sidebar.display()
