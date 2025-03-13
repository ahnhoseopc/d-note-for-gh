import utils.auth as auth
import utils.qna as qna
import forms.sidebar as sidebar
import views.gh_dinq_00 as intro

import streamlit as st

@auth.login_required
def main():
    # Initialize user id
    # if "user_id" not in st.session_state:
    #     st.session_state.user_id = "munhwa_user"

    #
    # Page title for D-QnA
    #
    st.title("D-INQ, 사전진료 Agent")

    tab0, tab1, tab2 = st.tabs(["사전진료 Agent", "**의료진**", "환자"])

    with tab0:
        intro.intro_record_source()

    with tab1:
        st.image("assets/dma/dinq-admin-serviceflow.png")

        st.markdown("## 의료진용 서비스 화면")
        st.image("assets/dma/dinq-admin.png", use_container_width=True, )
        st.image("assets/dma/dinq-admin-detail.png", use_container_width=True)

    with tab2:
        st.markdown("#### 환자용 서비스 화면")

        cols = st.columns([1,4])
        cols[0].markdown(" ")
        cols[0].markdown("###  진료정보 조회")
        cols[0].image("assets/dma/dinq_qr_dk.png", width=300)
        cols[0].link_button("진료정보 앱","https://devloginside.azurewebsites.net/dk", use_container_width=True)
        cols[1].image("assets/dma/dinq-app-serviceflow.png", use_container_width=True)


# import forms.sidebar as sidebar

if __name__ == "__page__":
    main()
    sidebar.display()
