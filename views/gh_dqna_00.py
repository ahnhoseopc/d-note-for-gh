import streamlit as st


DQNA_HELP = """전문의라고 할할지라도 본인의 전공분야가 아닌 타분야에 대한 의료지식 혹은 최신 학회정보 및 trend를 Update하기 위해서는 

일반인들이 문의하는 네이버, 구글의 일반검색과 다른 차별화된 의료진만의 전문 검색/문답서비스가 필요합니다.

이에 구글의 MedLM 기반의 질의응답서비스를 제공함으로써 의료진들의 질문의 맥락을 이해하고 의료진의 언어로 답을 줄 수 있는 서비스를 출시합니다.

필요없는 장황한 생성형 AI의 특성을 통한 무의미한 답변대신에 D-Q&A는 의사분들에게 짧고 핵심적인 언어로 답을 주고자 합니다.

매일매일 변화하는 의료환경에서 구글의 Medlm은 가장 적합하고 효과적인 가이드를 제공할 수 있습니다.
"""


def intro_record_source():
    cols = st.columns(2)
    with cols[0]:
        st.markdown("### D-QnA 설명서")
        st.markdown("    상단 Doctor's QnA 탭에서 의료관련 질문을 입력하세요.")
        st.markdown("    상단 Expert's QnA 탭에서 의료관련 질문을 입력하세요. (서비스 준비중)")
        st.markdown("    상단 Researcher's QnA 탭에서 의료논문 질문을 입력하세요. (서비스 준비중)")
        st.markdown("    왼쪽 사이드바에서 현재 질문 내용을 저장할 수 있습니다.")
    with cols[1]:
        st.markdown("### D-QnA 서비스는")
        st.markdown(DQNA_HELP)
