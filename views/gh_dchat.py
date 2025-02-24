import utils.auth as auth
import forms.sidebar_qna as sidebar_qna

import streamlit as st

DCHAT_HELP = """병원의 다양한 부서중에서 수익창출과 직접적으로 연관되어 있는 보험심사팀은 아주 중요한 업무를 담당하고 있습니다.

수시로 개정되는 고시를 Update하고, 임상과별 진료내역을 집계/청구하며, 심평원으로부터 통보된 다양한 feedback의 결과를 처리하는 병원의 매출과 제일 직접적으로 연관된 부서입니다.

이에 D-Chat을 통해, 1) 개정된 고시 Update 2) 심사부서 및 병원내 의료진에 대한 보험료 청구/삭감에 대한 문답서비스를 제공하고자 합니다.
특히 업무중 의료진으로부터 많은 질의에 대한 응답에 우선대응함으로써 보험심사팀 직원들의 업무집중도를 제고할 수 있습니다.

필요할 경우, 병원의 DB와 연결을 통해 병원만의 특화된 서비스도 가능합니다.
"""

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
    st.title("D-Chat, 전문 의료업무 정보 Agent", help=DCHAT_HELP)

    # 저장된 챗 메시지 출력 
    st.text(st.session_state.chat_name, help="채팅 제목")
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
