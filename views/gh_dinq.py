import utils.auth as auth
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
        st.markdown("### 의료진용 서비스 화면")
        with st.expander("의료진용 서비스 화면", expanded=False):
            dinq_doctor_url = "https://devma.azurewebsites.net/dk"
            html_code = f"""
            <iframe src="{dinq_doctor_url}" style="width:100%; height:900px; border:none;"></iframe>
            """
            st.markdown(html_code, unsafe_allow_html=True)
    
        cols = st.columns(5)
        cols[2].image("assets/dma/dinq-admin-page.png", width=200)
        cols[2].link_button("의료진용 서비스 화면", dinq_doctor_url, use_container_width=True)

        st.image("assets/dma/dinq-admin-serviceflow.png")

        st.markdown("##### 서비스 화면 샘플")
        st.image("assets/dma/dinq-admin.png")
        st.image("assets/dma/dinq-admin-detail.png")

    with tab2:
        st.markdown("### 환자용 서비스 화면")
        with st.expander("환자용 서비스 화면", expanded=False):
            dinq_patient_url = "https://devloginside.azurewebsites.net/hos/dk/"
            html_code = f"""
            <iframe src="{dinq_patient_url}" style="width:100%; height:900px; border:none;"></iframe>
            """
            st.markdown(html_code, unsafe_allow_html=True)

        cols = st.columns(5)
        cols[2].image("assets/dma/dinq_qr_dk.png", width=200)
        cols[2].link_button("환자용 서비스 화면", dinq_patient_url, use_container_width=True)

        st.image("assets/dma/dinq-app-serviceflow.png", use_container_width=True)


# import forms.sidebar as sidebar

if __name__ == "__page__":
    main()
    sidebar.display()
