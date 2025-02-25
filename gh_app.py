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

    # gh_api_page = st.Page(
    #     page="views/gh_dapi.py",
    #     title="D-API",
    #     icon=":material/question_exchange:",
    #     default=False
    # )

    # shared on all pages
    st.logo("assets/dma/dma.png", size="large")

    with st.sidebar.container():
        pg = st.navigation(
            {
                "About": [gh_about_dma_page, gh_about_gh_page],
                "DK Medical Agents": [gh_dnote_page, gh_dqna_page, gh_dchat_page, gh_dinq_page ],
                "Configuration (Admin)": [gh_dbquery_page],
            }
        )

    # Run Navigation
    pg.run()
    pass

print(f"gh_app.__name__: {__name__}")

# import services.dma_api as api
# from threading import Thread

# if "Fastapi" not in st.session_state:
#     st.session_state["Fastapi"] = "stopped"
# print(f"Fastapi 1: {st.session_state["Fastapi"]}")

# 메인 실행
if __name__ == "__main__":
    # print(f"Fastapi 2: {st.session_state["Fastapi"]}")
    # # FastAPI 서버 실행 (별도 스레드)
    # if st.session_state["Fastapi"] == "stopped":
    #     print(f">>> Fastapi start running")
    #     api_thread = Thread(target=api.run_fastapi, daemon=True)
    #     api_thread.start()
    #     st.session_state["Fastapi"] = "started"
    #     print(f"Fastapi 3: {st.session_state["Fastapi"]}")
    
    # Streamlit UI 실행
    dma_run()
    pass
