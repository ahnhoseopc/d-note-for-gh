import streamlit as st


DINQ_HELP = """병원을 처음 방문하는 초진환자들, 특히 나이가 많은 시니어분, 나이 어린 소아환자들,태아를 임신한 여자환자분, 약물에 부작용이 있거나 조영제사용이 필요한 환자분들에게는 환자의 과거 치료 내역이 아주 중요합니다.

어떤 약을 복용했고 어떤 수술기록이 있었는지 대부분의 환자는 의학적인 지식이 부족하여 의사에게 본인의 정확한 status를 전달하기 어렵습니다.

이에 DK는 심평원의 과거 5년동안의 복용/수술내역을 Data화하여 의료진에게 제공할 수 있는 D-INQ라는 서비스를 제공하고자 합니다.

심평원의 방대한 Raw data를 질병과 복용내역과 Matching하여 제공하는 기술은 상당한 노하우가 필요한 작업입니다. 차별화된 기능을 통해 의료진은 환자에게 맞춤형 의료서비스를 제공하여 타 병원과 차별화된 서비스 제공이 가능합니다.

"""


def intro_record_source():
    cols = st.columns(2)
    with cols[0]:
        st.markdown("### D-INQ 설명서")
        st.markdown("    사용을 위해서는 DMA 담당자에게 연락 부탁드립니다.")
        st.markdown("    - DK와 협의를 거친후 고객를 위한 사이트 주소가 할당이 됩니다.")
        st.markdown("    - 의료진 및 관리자가 사용할 계정이 할당이 됩니다.")
        st.markdown("    - 환자에게 안내할 모바일 앱 및 QR코드가 안내됩니다.")
        st.markdown("    - 보안을 위해 사이트 접속이 특정 장소 또는 IP로 한정됩니다.")
    with cols[1]:
        st.markdown("### D-INQ 서비스는")
        st.markdown(DINQ_HELP)
