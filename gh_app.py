import streamlit as st

def dma_run():
    st.set_page_config(layout="wide")

    # page setup
    gh_about_page = st.Page(
        page="views/gh_about.py",
        title="About Good Hospitals",
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
        default=False
    )

    gh_dqna_page = st.Page(
        page="views/gh_dqna.py",
        title="D-QnA",
        icon=":material/question_exchange:",
        default=False
    )

    gh_api_page = st.Page(
        page="views/callapi.py",
        title="D-API",
        icon=":material/question_exchange:",
        default=True
    )

    # shared on all pages
    st.logo("assets/gh_logo.png", size="large")

    with st.sidebar.container():
        pg = st.navigation(
            {
                "Info": [gh_about_page],
                "DK Medical Agents": [gh_dnote_page, gh_dqna_page, gh_api_page],
                "Configuration (Admin)": [gh_dbquery_page],
            }
        )

    # Run Navigation
    pg.run()
    pass

import utils.api as api
from threading import Thread

# 메인 실행
if __name__ == "__main__":
    # FastAPI 서버 실행 (별도 스레드)
    api_thread = Thread(target=api.run_fastapi, daemon=True)
    api_thread.start()
    
    # Streamlit UI 실행
    dma_run()
