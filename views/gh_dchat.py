import utils.auth as auth
import forms.sidebar_qna as sidebar_qna
import utils.qna as qna
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

    tab0, tab1, tab2, tab3 = st.tabs(["의료업무 정보화 Agent", "**요양급여규정 안내**", "보험심사청구 업무", "상병코드 매핑"])

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
            st.markdown("#### Recommended questions")
            st.markdown("1. Questions 2")
            st.markdown("2. Questions 3")
            st.markdown("3. Questions 4")
            st.markdown("4. Questions 5")
            pass

    with tab3:
        col1, col2 = st.columns([8,2])
        with col1:
            st.markdown("""
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: none !important;
            padding: 10px;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)
            st.markdown("""
<table width="100%">
<tr>
<td align="left" width="25%">

**등록번호**: {}  
**진 료 과**: {}  

</td>
<td align="center" width="50%">

### 입원기록지 ( Addmission Note )
Date of Admission: {}

</td>
<td align="right" width="25%">
<img src="http://www.goodhospital.or.kr/goodtimes/images_new/logo.png" alt="좋은병원들" width="120">  
</td>
</tr>
</table>

""", unsafe_allow_html=True)
            st.markdown("##### 상병코드  ")
            st.caption(f"KCD 001002")
            st.markdown("##### 상병코드상세  ")
            st.caption(f"KCD 상병명 한글")
            st.caption(f"KCD 상병명 영문")
            if "chief_complaint" not in st.session_state: st.session_state.chief_complaint = ""
            if "present_illness" not in st.session_state: st.session_state.present_illness = ""
            if "impression" not in st.session_state: st.session_state.impression = ""
            st.text_area("주호소", value=st.session_state.chief_complaint, height=100, key="cc")
            st.text_area("현증상", value=st.session_state.present_illness, height=100, key="pi")
            st.text_area("소견", value=st.session_state.impression, height=100, key="imp")
            pass

        with col2:
            st.markdown("#### Recommended questions")
            st.markdown("1. Questions 2")
            st.markdown("2. Questions 3")
            st.markdown("3. Questions 4")
            st.markdown("4. Questions 5")
            pass


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
