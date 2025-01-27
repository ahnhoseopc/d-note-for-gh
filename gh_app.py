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
    icon=":material/bar_chart:",
    default=False
)

gh_dnote_page = st.Page(
    page="views/gh_dnote.py",
    title="D-Note",
    icon=":material/smart_toy:",
    default=True
)

pg = st.navigation(
    {
        "Info": [gh_about_page],
        "Projects": [gh_dbquery_page, gh_dnote_page],
    }
)

# shared on all pages
st.logo("assets/gh_logo.png", size="large")
with st.sidebar:
    cols = st.columns([3,1])
    with cols[0]: st.text("Provided by ")
    with cols[1]: st.image("assets/dk_logo.png", width=40)

# Run Navigation
pg.run()
