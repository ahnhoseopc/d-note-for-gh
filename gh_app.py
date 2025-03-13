import streamlit as st

def dma_run():
    st.set_page_config(page_title="Good Hospitals - DK Medical Agents", page_icon="🏥", layout="wide")

    # shared on all pages
    st.logo("assets/dma/dk_hospital_logo.png", size="large")
    
    # page setup
    gh_about_dma_page = st.Page(
        page="views/gh_about_dma.py",
        title="DMA",
        icon=":material/account_circle:",
        default=True
    )

    gh_about_partners_page = st.Page(
        page="views/gh_about_partners.py",
        title="Partners",
        icon=":material/partner_exchange:",
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
        default=False
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
        title="D-INQ",
        icon=":material/medical_information:",
        default=False
    )

    # Main menu for DMA
    menu = {
            "About": [gh_about_dma_page, gh_about_partners_page],
            "DK Medical Agents": [gh_dnote_page, gh_dqna_page, gh_dchat_page, gh_dinq_page ],
        }

    # Menu for admin
    if "user_id" in st.session_state and st.session_state.user_id == "dma":
        menu["Configuration (Admin)"] = [gh_dbquery_page]

    with st.sidebar.container():
        pg = st.navigation(menu)

    # Run Navigation
    pg.run()
    pass

# 메인 실행
if __name__ == "__main__":
    dma_run()
    pass
