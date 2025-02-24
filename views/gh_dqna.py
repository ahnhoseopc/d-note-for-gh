import utils.auth as auth
import utils.qna as qna
import forms.sidebar_qna as sidebar_qna

import streamlit as st

DQNA_HELP = """전문의라고 할할지라도 본인의 전공분야가 아닌 타분야에 대한 의료지식 혹은 최신 학회정보 및 trend를 Update하기 위해서는 

일반인들이 문의하는 네이버, 구글의 일반검색과 다른 차별화된 의료진만의 전문 검색/문답서비스가 필요합니다.

이에 구글의 MedLM 기반의 질의응답서비스를 제공함으로써 의료진들의 질문의 맥락을 이해하고 의료진의 언어로 답을 줄 수 있는 서비스를 출시합니다.

필요없는 장황한 생성형 AI의 특성을 통한 무의미한 답변대신에 D-Q&A는 의사분들에게 짧고 핵심적인 언어로 답을 주고자 합니다.

매일매일 변화하는 의료환경에서 구글의 Medlm은 가장 적합하고 효과적인 가이드를 제공할 수 있습니다.
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
    st.title("D-QnA, 전문 의료지식 정보화 Agent", help=DQNA_HELP)

    tab0, tab1, tab2, tab4 = st.tabs(["의료지식 정보화 Agent", "**Doctor's**", "Professional's", "Researcher's"])

    with tab0:
        st.markdown(DQNA_HELP)

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
