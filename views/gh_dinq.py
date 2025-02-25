import utils.auth as auth
import utils.qna as qna
import forms.sidebar_qna as sidebar_qna
import views.gh_dinq_00 as intro

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
    st.title("D-INQ, 사전진료 Agent")

    tab0, tab1, tab2 = st.tabs(["사전진료 Agent", "**의료진**", "환자"])

    with tab0:
        intro.intro_record_source()

    with tab1:
        st.image("assets/dma/dinq-admin-serviceflow.png")

        st.image("assets/dma/dinq-admin.png")
        st.image("assets/dma/dinq-admin-detail.png")

    with tab2:
        st.image("assets/dma/dinq-app-serviceflow.png")

        st.image("assets/dma/dinq-app.png")

# import forms.sidebar as sidebar

if __name__ == "__page__":
    main()
    # sidebar.display()
