import streamlit as st

# page setup
gh_about_page = st.Page(
    page="views/gh_about.py",
    title="About Good Hospital",
    icon=":material/account_circle:",
    default=True
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
    default=False
)

pg = st.navigation(
    {
        "Info": [gh_about_page],
        "Projects": [gh_dbquery_page, gh_dnote_page],
    }
)

# shared on all pages
st.logo("assets/dk_logo.png")
st.sidebar.text("Provided by DK+")

# Run Navigation
pg.run()
