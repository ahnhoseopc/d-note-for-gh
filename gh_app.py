import streamlit as st

def dma_run():
    st.set_page_config(layout="wide")

    # page setup
    gh_about_dma_page = st.Page(
        page="views/gh_about_dma.py",
        title="DMA",
        icon=":material/account_circle:",
        default=False
    )

    gh_about_gh_page = st.Page(
        page="views/gh_about_gh.py",
        title="Good Hospitals",
        icon=":material/account_circle:",
        default=False
    )

    gh_dbquery_page = st.Page(
        page="views/gh_dbquery.py",
        title="Database Query",
        icon=":material/data_object:",
        default=False
    )

    gh_dnote_page = st.Page(
        page="views/gh_dnote.py",
        title="D-Note",
        icon=":material/clinical_notes:",
        default=True
    )

    gh_dqna_page = st.Page(
        page="views/gh_dqna.py",
        title="D-QnA",
        icon=":material/question_exchange:",
        default=False
    )

    gh_dchat_page = st.Page(
        page="views/gh_dchat.py",
        title="D-Chat",
        icon=":material/chat:",
        default=False
    )

    gh_dinq_page = st.Page(
        page="views/gh_dinq.py",
        title="D-INQuiry",
        icon=":material/medical_information:",
        default=False
    )

    # shared on all pages
    st.logo("assets/dma/dma.png", size="large")

    if "user_id" in st.session_state and st.session_state.user_id == "dma":
        menu = {
                "About": [gh_about_dma_page, gh_about_gh_page],
                "DK Medical Agents": [gh_dnote_page, gh_dqna_page, gh_dchat_page, gh_dinq_page ],
                "Configuration (Admin)": [gh_dbquery_page],
            }
    else:
        menu = {
                "About": [gh_about_dma_page, gh_about_gh_page],
                "DK Medical Agents": [gh_dnote_page, gh_dqna_page, gh_dchat_page, gh_dinq_page ],
            }

    with st.sidebar.container():
        pg = st.navigation(menu)

    # Run Navigation
    pg.run()
    pass

# 메인 실행
if __name__ == "__main__":
    dma_run()
    pass
