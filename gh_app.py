import forms.login as login

import random
import streamlit as st

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
    default=True
)

# shared on all pages
st.logo("assets/gh_logo.png", size="large")

with st.sidebar.container():
    pg = st.navigation(
        {
            "Info": [gh_about_page],
            "DK Medical Agents": [gh_dnote_page, gh_dqna_page],
            "Configuration (Admin)": [gh_dbquery_page],
        }
    )

# sidebar_slot = st.sidebar.container(height=300)

# if "sidebar_slot" not in st.session_state:
#     st.session_state.sidebar_slot = sidebar_slot

# with st.sidebar.container():
#     cols = st.columns([1,1,1])
#     with cols[0]: st.metric("Grade", value=random.randint(80,99))
#     with cols[1]: st.metric("Index", value=random.randint(80,99))
#     with cols[2]: st.metric("Count", value=random.randint(150,199))
#     cols = st.columns([3,1])
#     with cols[0]: st.text("Provided by ")
#     with cols[1]: st.image("assets/dk_logo.png", width=40)

# Run Navigation
pg.run()
