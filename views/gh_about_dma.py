import streamlit as st

def main():
    st.header("DK Medical Agents - DMA", anchor="network", divider="orange")

    st.image("assets/00_dma_main.jpg", use_container_width=True)

    cols = st.columns(2)
    with cols[0]:
        st.markdown("## DMA 서비스는?")

        st.markdown("- 국내 최초의 Medical 분야, 생성형 AI기반 서비스", unsafe_allow_html=True)

        st.markdown("- 병원의 의료진 & 행정근무부서 대상, Non-clinical 분야 서비스", unsafe_allow_html=True)

        st.markdown("- 구글의 Medical 전문 Foundation 기반, 특화 서비스", unsafe_allow_html=True)

        st.markdown("- Cloud 기반의 월정액 구독 서비스", unsafe_allow_html=True)

        st.markdown("## DMA 고객은?")

        st.markdown("- Front 부서: 병원의 의료진(전문의, 수련의, 간호사 대상)", unsafe_allow_html=True)

        st.markdown("- Desk 부서: 보험심사팀, 원무팀, 행정지원부서", unsafe_allow_html=True)

    with cols[1]:
        st.markdown("## DMA 차별화 포인트")

        st.markdown("""1. Quality care """, unsafe_allow_html=True)
        st.markdown("""  - 의료진이 환자 진료에 집중하게 함으로써 “환자만족도” 제고 """, unsafe_allow_html=True)
        st.markdown("""  - 비임상분야의 단순,반복,과다시간 소요되는 업무를 자동화 """, unsafe_allow_html=True)

        st.markdown("""2. 구독 Base 서비스 """, unsafe_allow_html=True)
        st.markdown("""  - 초기투자비용, 관리비용(장비/인력)성격의 고정비 지출 부담에서 탈피 """, unsafe_allow_html=True)
        st.markdown("""  - 서비스에 불만이 있을 경우, 언제든 해지가능한 고객중심 서비스 """, unsafe_allow_html=True)

        st.markdown("""3. 병원 맞춤형 /적시성 서비스 """, unsafe_allow_html=True)
        st.markdown("""  - 병원마다 특화된 Needs에 대한 맞춤형 서비스 제공가능(RAG,Appsheet) """, unsafe_allow_html=True)
        st.markdown("""  - 설치형 제품과 달리 항시 적시 Update 정보 제공 """, unsafe_allow_html=True)

        st.markdown("- Desk 부서: 보험심사팀, 원무팀, 행정지원부서", unsafe_allow_html=True)



import forms.sidebar as sidebar

if __name__ == "__page__":
    main()
    sidebar.display()
