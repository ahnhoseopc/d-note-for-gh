import streamlit as st

import base64

# 이미지 파일을 Base64로 변환하는 함수
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def main():
    st.header("DMA Partners", anchor="network", divider="orange")

    # 프로젝트 내부 이미지 경로
    partners = [("assets/dma/partner-google-cloud_logo.svg", "Google", "전세계 최고 클라우드 기업"), 
                ("assets/dma/partner-tpcg_logo.png", "TPCG", "국내 최고 수준의 전문 AI 기업"), 
                ("assets/dma/partner-ghc_logo.svg", "Grade Health Chain", "건강, 보험 분야의 최고 데이터 관리 기업"), 
                ("assets/dma/partner-kcube_logo.png", "Knowledge Cube", "GWS와 최고의 궁합을 보여주는 그룹웨어 솔루션 기업"), 
                ("assets/dma/partner-oktomato_logo.svg", "OK 토마토", "탑티어 시스템 통합 솔루션 Maker")]

    if "partner_index" not in st.session_state:
        st.session_state.partner_index = 0

    cols = st.columns([2,4,2], vertical_alignment="center")
    with cols[0]:
        col0 = st.columns(3, vertical_alignment="center")
        with col0[1]:
            if st.button("<"):
                st.session_state.partner_index = (st.session_state.partner_index - 1) % len(partners)

    with cols[2]:
        # 변경된 이미지 인덱스가 이미지 출력에 여향을 주도록 cols[1] 보다 cols[2]가 먼저 위치함.
        col2 = st.columns(3, vertical_alignment="center")
        with col2[1]:
            if st.button("\\>"):
                st.session_state.partner_index = (st.session_state.partner_index + 1) % len(partners)

    with cols[1]:
        partner_index = st.session_state.partner_index
        image_file = partners[partner_index][0]
        st.image(image_file, use_container_width=True)
        # st.markdown(f"##### {partners[partner_index][1]}")
        # st.markdown(f"  {partners[partner_index][2]}")

    cols = st.columns([3,2])
    with cols[0]:
        st.markdown("## DMA 파트너들은?")

        st.markdown(f"- {partners[0][1]}, {partners[0][2]}", unsafe_allow_html=True)

        st.markdown(f"- {partners[1][1]}, {partners[1][2]}", unsafe_allow_html=True)

        st.markdown(f"- {partners[2][1]}, {partners[2][2]}", unsafe_allow_html=True)

        st.markdown(f"- {partners[3][1]}, {partners[3][2]}", unsafe_allow_html=True)

        st.markdown(f"- {partners[4][1]}, {partners[4][2]}", unsafe_allow_html=True)


    with cols[1]:
        colx = st.columns(2)
        st.markdown("####  ")
        st.image(partners[0][0], width=100)
        st.image(partners[1][0], width=100)
        st.image(partners[2][0], width=100)
        st.image(partners[3][0], width=100)
        st.image(partners[4][0], width=100)


import forms.sidebar as sidebar

if __name__ == "__page__":
    main()
    sidebar.display()
